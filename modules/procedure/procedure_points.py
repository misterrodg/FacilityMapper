from modules.db.joined_procedure_records import JoinedProcedureRecords
from modules.db.record_helper import (
    cast_from_to,
    revert_from_to,
    segment_records,
)
from modules.procedure.procedure_point import ProcedurePoint


class ProcedurePoints:
    records: list[ProcedurePoint]

    def __init__(self, records: list[ProcedurePoint]) -> None:
        self.records = []
        self.records.extend(records)

    @classmethod
    def from_point_list(cls, points: list[ProcedurePoint]) -> "ProcedurePoints":
        return cls(points)

    @classmethod
    def from_joined_records(
        cls, joined_records: JoinedProcedureRecords
    ) -> "ProcedurePoints":
        records: list[ProcedurePoint] = []
        for record in joined_records.get_records():
            procedure_point = ProcedurePoint(
                fix_id=record.fix_id,
                fix_lat=record.fix_lat,
                fix_lon=record.fix_lon,
                fix_source=record.fix_source,
                fix_type=record.fix_type,
                fix_mag_var=record.fix_mag_var,
                symbol_name=record.fix_type_to_symbol_name(),
                procedure_id=record.procedure_id,
                procedure_type=record.procedure_type,
                fac_sub_code=record.fac_sub_code,
                transition_id=record.transition_id,
                seq_no=record.seq_no,
                path_term=record.path_term,
                course=record.course,
                center_fix=record.center_fix,
                center_lat=record.center_lat,
                center_lon=record.center_lon,
                arc_radius=record.arc_radius,
                turn_direction=record.turn_direction,
                desc_code=record.desc_code,
                alt_desc=record.alt_desc,
                alt_1=record.alt_1,
                fl_1=bool(record.fl_1),
                alt_2=record.alt_2,
                fl_2=bool(record.fl_2),
                speed_desc=record.speed_desc,
                speed_limit=record.speed_limit,
            )
            if (
                procedure_point.fix_lat is not None
                and procedure_point.fix_lon is not None
            ):
                records.append(procedure_point)
        return cls(records)

    def get_records(self) -> list[ProcedurePoint]:
        return self.records

    def __bool__(self) -> bool:
        return bool(self.records)

    def split_paths(self) -> list["ProcedurePoints"]:
        paths: list[ProcedurePoints] = []
        for segment in segment_records(self.records, ProcedurePoint.SEGMENT_FIELD):
            if segment:
                paths.append(ProcedurePoints.from_point_list(segment))
        return paths

    def get_from_to(self) -> list[tuple[ProcedurePoint, ProcedurePoint]]:
        return cast_from_to(self.records)

    @staticmethod
    def _split_on_none(
        list_to_verify: list[tuple[ProcedurePoint, ProcedurePoint] | None],
    ) -> list[list[tuple[ProcedurePoint, ProcedurePoint]]]:
        result: list[list[tuple[ProcedurePoint, ProcedurePoint]]] = []
        temporary: list[tuple[ProcedurePoint, ProcedurePoint]] = []

        for item in list_to_verify:
            if item is not None:
                temporary.append(item)
            else:
                if temporary:
                    result.append(temporary)
                    temporary = []

        if temporary:
            result.append(temporary)

        return result

    @staticmethod
    def _dedupe_from_to_paths(
        paths: list["ProcedurePoints"],
        drop_self_pairs: bool,
    ) -> list[list[tuple[ProcedurePoint, ProcedurePoint]]]:
        result: list[list[tuple[ProcedurePoint, ProcedurePoint]]] = []
        seen: list[str] = []

        for path in paths:
            unique: list[tuple[ProcedurePoint, ProcedurePoint] | None] = []
            for record_from, record_to in path.get_from_to():
                pair = f"{record_from.fix_id}-{record_to.fix_id}"
                value = None
                is_self_pair = record_from.fix_id == record_to.fix_id
                if pair not in seen and (not drop_self_pairs or not is_self_pair):
                    seen.append(pair)
                    value = (record_from, record_to)
                unique.append(value)
            if unique:
                result.extend(ProcedurePoints._split_on_none(unique))

        return result

    def get_segmented_records(self) -> list[list[ProcedurePoint]]:
        return [path.get_records() for path in self.split_paths()]

    def get_segmented_from_to(
        self,
    ) -> list[list[tuple[ProcedurePoint, ProcedurePoint]]]:
        result: list[list[tuple[ProcedurePoint, ProcedurePoint]]] = []
        for path in self.split_paths():
            from_to = path.get_from_to()
            if from_to:
                result.append(from_to)
        return result

    def get_unique_paths(self) -> list[list[ProcedurePoint]]:
        result: list[list[ProcedurePoint]] = []
        unique_paths_from_to = ProcedurePoints._dedupe_from_to_paths(
            self.split_paths(),
            drop_self_pairs=False,
        )
        for path_from_to in unique_paths_from_to:
            result.append(revert_from_to(path_from_to))

        return result

    def get_unique_paths_from_to(
        self,
    ) -> list[list[tuple[ProcedurePoint, ProcedurePoint]]]:
        return ProcedurePoints._dedupe_from_to_paths(
            self.split_paths(),
            drop_self_pairs=True,
        )

    def trim_missed(self, keep_runway: bool = False) -> None:
        result: list[ProcedurePoint] = []
        missed_reached = False
        for record in self.records:
            fix_id = record.fix_id
            is_runway_fix = isinstance(fix_id, str) and fix_id.startswith("RW")
            if not missed_reached and (keep_runway or not is_runway_fix):
                result.append(record)

            desc_code = record.desc_code
            if isinstance(desc_code, str) and len(desc_code) > 3 and desc_code[3] == "M":
                missed_reached = True

        self.records = result

    def add_procedure_name_to_enroute_transitions(self) -> None:
        for record in self.records:
            if (
                record.fix_id is not None
                and record.procedure_id is not None
                and record.fix_id == record.transition_id
            ):
                record.fix_id = f"{record.procedure_id}.{record.fix_id}"

    def add_procedure_name_to_core(self, last: bool = False) -> None:
        if not self.records:
            return

        record = self.records[-1] if last else self.records[0]
        if record.procedure_id is None or record.fix_id is None:
            return

        record.fix_id = f"{record.procedure_id}.{record.fix_id}"

    def add_procedure_name_to_runway_transitions(self) -> None:
        for record in self.records:
            if (
                record.fix_id is not None
                and record.procedure_id is not None
                and record.fix_id == record.procedure_id[:-1]
            ):
                record.fix_id = f"{record.procedure_id}.{record.fix_id}"
