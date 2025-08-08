from modules.v_nas import LINE_STYLE_SOLID


class LineOptions:
    buffer_length: float
    style: str
    vector_length: float

    def __init__(
        self,
        buffer_length: float = 0.0,
        style: str = LINE_STYLE_SOLID,
        vector_length: float = 0.0,
    ):
        self.buffer_length = buffer_length
        self.style = style
        self.vector_length = vector_length


class SymbolOptions:
    as_lines: bool
    scale: float

    def __init__(self, as_lines: bool = False, scale: float = 1.0):
        self.as_lines = as_lines
        self.scale = scale


class TextOptions:
    draw_names: bool
    draw_altitudes: bool
    draw_speeds: bool
    as_lines: bool
    x_offset: float
    y_offset: float
    scale: float
    line_height: float

    def __init__(
        self,
        draw_names: bool = False,
        draw_altitudes: bool = False,
        draw_speeds: bool = False,
        as_lines: bool = False,
        x_offset: float = 0.0,
        y_offset: float = 0.0,
        scale: float = 1.0,
        line_height: float = 1.0,
    ):
        self.draw_names = draw_names
        self.draw_altitudes = draw_altitudes
        self.draw_speeds = draw_speeds
        self.as_lines = as_lines
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.scale = scale
        self.line_height = line_height
