from modules.ErrorHelper import print_top_level
from modules.vNAS import LINE_STYLES

ERROR_HEADER = "SID/STAR: "


class SIDSTAR:
    def __init__(self, mapType: str, definitionDict: dict):
        self.mapType = mapType
        self.airportId = None
        self.procedureId = None
        self.lineStyle = None
        self.drawSymbols = False
        self.drawNames = False
        self.fileName = None

        self.validate(definitionDict)

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

        fileName = definitionDict.get("file_name")
        if fileName is None:
            fileName = f"{airportId}_{self.mapType}_{procedureId}"

        self.airportId = airportId
        self.procedureId = procedureId
        self.lineStyle = lineStyle
        self.drawSymbols = drawSymbols
        self.drawNames = drawNames
        self.fileName = fileName

        return
