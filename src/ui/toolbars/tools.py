from enum import Enum


class Mode(Enum):
    DRAW = "Draw"
    ICON = "Icon"
    TEXT = "Text"

class DrawTool(Enum):
    FREEHAND = "🖊️"
    RECT_ADD = "🔲"
    RECT_DRAG = "🔲↔️"
    CIRCLE_ADD = "⚪"
    CIRCLE_DRAG = "⚪↔️"
    PATH_DRAW = "╲"
    POLYGON_DRAW = "△🖊️"
    POLYGON_DRAG = "△↔"
    GRID_RECT_ADD = "Grid"

class IconTool(Enum):
    ADD_ICON = "+"
    REMOVE_ICON = "-"

class TextTool(Enum):
    ADD_TEXT = "+"
    REMOVE_TEXT = "-"

class LayerTool(Enum):
    ADD_LAYER = "Neue Ebene"
    REMOVE_LAYER = "Ebene löschen"
    GO_UP = "Hoch"
    GO_DOWN = "Runter"
    RENAME = "Umbenennen"

def get_tools(mode):
    if mode == Mode.DRAW:
        return DrawTool
    if mode == Mode.ICON:
        return IconTool
    if mode == Mode.TEXT:
        return TextTool

