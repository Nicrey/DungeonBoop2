from enum import Enum


class Mode(Enum):
    DRAW = "Draw"
    ICON = "Icon"
    TEXT = "Text"

class DrawTool(Enum):
    FREEHAND = "🖊️"
    RECT_ADD = "R+"
    RECT_DRAG = "RD"
    CIRCLE_ADD = "C+"
    CIRCLE_DRAG = "CD"
    PATH_DRAW = "P"
    POLYGON_DRAW = "POL"
    GRID_RECT_ADD = "GR+"

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

