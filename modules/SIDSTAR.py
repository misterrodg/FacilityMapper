from modules.ErrorHelper import print_top_level
from modules.GeoJSON import (
    CoordinatePair,
    Feature,
    FeatureCollection,
    GeoJSON,
    LineString,
    MultiLineString,
)
from modules.QueryHelper import translateWildcard, segmentQuery
from modules.TextDraw import ARC_MIN, TextDraw
from modules.vNAS import LINE_STYLES

from sqlite3 import Cursor

ERROR_HEADER = "SID/STAR: "


class SIDSTAR:
    def __init__(self, dbCursor: Cursor, mapType: str, definitionDict: dict):
        self.mapType = mapType
        self.airportId = None
        self.procedureId = None
        self.lineStyle = None
        self.drawSymbols = False
        self.drawNames = False
        self.xOffset = None
        self.yOffset = None
        self.textScale = None
        self.drawEnrouteTransitions = True
        self.drawRunwayTransitions = False
        self.fileName = None
        self.dbCursor = dbCursor

        self.validate(definitionDict)
        self._toFile()

    def validate(self, definitionDict: dict) -> None:
        airportId = definitionDict.get("airport_id")
        if airportId is None:
            print(
                f"{ERROR_HEADER}Missing `airport_id` in:\n{print_top_level(definitionDict)}."
            )
            return

        procedureId = definitionDict.get("procedure_id")
        if procedureId is None:
            print(
                f"{ERROR_HEADER}Missing `procedure_id` in:\n{print_top_level(definitionDict)}."
            )
            return

        lineStyle = definitionDict.get("line_type", "solid")
        if lineStyle not in LINE_STYLES:
            print(f"{ERROR_HEADER}line_type '{lineStyle}' not recognized.")
            print(f"{ERROR_HEADER}Supported types are {", ".join(LINE_STYLES)}.")
            return

        drawSymbols = definitionDict.get("draw_symbols", False)

        drawNames = definitionDict.get("draw_names", False)

        xOffset = definitionDict.get("x_offset", 0) * ARC_MIN

        yOffset = definitionDict.get("y_offset", 0) * ARC_MIN

        textScale = definitionDict.get("text_scale", 1.0) * ARC_MIN

        drawEnrouteTransitions = definitionDict.get("draw_enroute_transitions", True)

        drawRunwayTransitions = definitionDict.get("draw_runway_transitions", False)

        fileName = definitionDict.get("file_name")
        if fileName is None:
            fileName = f"{airportId}_{self.mapType}_{procedureId}"

        self.airportId = airportId
        self.procedureId = procedureId
        self.lineStyle = lineStyle
        self.drawSymbols = drawSymbols
        self.drawNames = drawNames
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.textScale = textScale
        self.drawEnrouteTransitions = drawEnrouteTransitions
        self.drawRunwayTransitions = drawRunwayTransitions
        self.fileName = fileName

        return

    def _mapTypeToFacSubCode(self) -> str:
        result = ""
        if self.mapType == "SID":
            result = "'D'"
        if self.mapType == "STAR":
            result = "'E'"
        return result

    def _optionsToRouteType(self) -> str:
        result = ["'2','5'"]

        if self.mapType == "SID":
            if self.drawRunwayTransitions:
                result = ["'1','4'"] + result
            if self.drawEnrouteTransitions:
                result = result + ["'3','6'"]

        if self.mapType == "STAR":
            if self.drawEnrouteTransitions:
                result = ["'1','4'"] + result
            if self.drawRunwayTransitions:
                result = result + ["'3','6'"]

        result = ",".join(result)
        return result

    def _toQuery(self) -> str:
        fac_id = f"'{self.airportId}'"
        fac_sub_code = self._mapTypeToFacSubCode()
        procedure_id = f"'{translateWildcard(self.procedureId)}'"
        route_type = self._optionsToRouteType()

        return f"""
        WITH unified_table AS (
            SELECT waypoint_id AS id,lat,lon FROM waypoints
            UNION
            SELECT vhf_id AS id,lat,lon FROM vhf_dmes
        )
        SELECT p.fac_id,p.fac_sub_code,p.procedure_id,p.transition_id,p.route_type,p.sequence_number,p.fix_id,lat,lon
        FROM procedure_points AS p
        JOIN unified_table AS u ON p.fix_id = u.id
        WHERE fac_id = {fac_id} AND fac_sub_code={fac_sub_code} AND procedure_id LIKE {procedure_id} AND route_type IN ({route_type})
        ORDER BY p.procedure_id,p.transition_id,p.route_type,p.sequence_number;
        """

    def _queryDB(self) -> list:
        query = self._toQuery()
        self.dbCursor.execute(query)
        result = self.dbCursor.fetchall()
        return result

    def _getLineStrings(self, rows: list) -> MultiLineString:
        segmentList = segmentQuery(rows, "transition_id")
        multiLineString = MultiLineString()
        for segmentItem in segmentList:
            lineString = LineString()
            for segment in segmentItem:
                coordinatePair = CoordinatePair(segment.get("lat"), segment.get("lon"))
                lineString.addCoordinatePair(coordinatePair)
            multiLineString.addLineString(lineString)

        return multiLineString

    def _getTextFeatures(self, rows: list) -> list[Feature]:
        seenIds = set()
        filteredRows = []
        for row in rows:
            if row["fix_id"] not in seenIds:
                filteredRows.append(row)
                seenIds.add(row["fix_id"])

        result = []
        for row in filteredRows:
            offsetLat = self.yOffset + row["lat"]
            offsetLon = self.xOffset + row["lon"]
            textDraw = TextDraw(row["fix_id"], offsetLat, offsetLon, self.textScale)
            result.append(textDraw.getFeature())

        return result

    def _toFile(self) -> None:
        rows = self._queryDB()
        multiLineString = self._getLineStrings(rows)

        feature = Feature()
        feature.addMultiLineString(multiLineString)

        featureCollection = FeatureCollection()
        featureCollection.addFeature(feature)

        if self.drawNames:
            featureArray = self._getTextFeatures(rows)
            for feature in featureArray:
                featureCollection.addFeature(feature)

        geoJSON = GeoJSON(self.fileName)
        geoJSON.addFeatureCollection(featureCollection)
        geoJSON.toFile()
