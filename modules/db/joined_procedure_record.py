from modules.db.procedure_record import ProcedureRecord
from typing import Any


class JoinedProcedureRecord(ProcedureRecord):
    fix_lat: float | None
    fix_lon: float | None
    fix_source: str | None
    fix_type: str | None
    fix_mag_var: float | None
    rec_vhf_id: str | None
    rec_vhf_lat: float | None
    rec_vhf_lon: float | None
    center_id: str | None
    center_lat: float | None
    center_lon: float | None

    def __init__(self, db_record: dict[str, Any]):
        super().__init__(db_record)
        self.fix_lat = db_record.get("fix_lat")
        self.fix_lon = db_record.get("fix_lon")
        self.fix_source = db_record.get("fix_source")
        self.fix_type = db_record.get("fix_type")
        self.fix_mag_var = db_record.get("fix_mag_var")
        self.rec_vhf_id = db_record.get("rec_vhf_id")
        self.rec_vhf_lat = db_record.get("rec_vhf_lat")
        self.rec_vhf_lon = db_record.get("rec_vhf_lon")
        self.center_id = db_record.get("center_id")
        self.center_lat = db_record.get("center_lat")
        self.center_lon = db_record.get("center_lon")

    def fix_type_to_symbol_name(self, use_faf_symbol: bool = False) -> str | None:
        if self.fix_type is None:
            return None

        if use_faf_symbol and self.desc_code is not None and self.desc_code.endswith("F"):
            return "FAF"

        source = self.fix_source
        row_type = self.fix_type
        if row_type is None:
            return None

        if source and source in ["ENR", "TRM"]:
            if self.fix_type.startswith("W"):
                return "RNAV_POINT"
            if self.fix_type.startswith("C") or self.fix_type.startswith("R"):
                return "WAYPOINT"

        if source and source == "VHF":
            if self.fix_type.startswith("VD"):
                return "VORDME"
            if self.fix_type.startswith("VT"):
                return "VORTAC"
            if self.fix_type.startswith("V "):
                return "VOR"
            if self.fix_type.startswith(" D"):
                return "DME"

        if source and source == "NDB":
            if self.fix_type.startswith("H"):
                return "NDB"

        return None
