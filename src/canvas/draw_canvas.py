from PySide6.QtWidgets import ( QWidget)
from PySide6.QtGui import QPainter, QPixmap, QPen, QBrush, QMouseEvent, QImage, QColor
from PySide6.QtCore import Qt, QPoint, QRect


from canvas.draw_tools.circle_drag import CircleDrag
from canvas.draw_tools.circle_inserter import CircleInserter
from canvas.draw_tools.freehand_draw import FreehandDraw
from canvas.draw_tools.freehand_erase import FreehandEraser
from canvas.draw_tools.grid_rect_drawer import GridRectDraw
from canvas.draw_tools.grid_rect_eraser import GridRectErase
from canvas.draw_tools.path_tool import PathTool
from canvas.draw_tools.polygon_tool import PolygonTool
from canvas.draw_tools.rect_drag import RectDrag
from canvas.draw_tools.rect_inserter import RectInserter
from ui.toolbars.tools import DrawTool


class DrawCanvas(QWidget):

    def __init__(self, parent_display=None):
        super().__init__()
        self.parent_display = parent_display  # Reference to CanvasController

        # Initialize the drawing surface
        self.pixmap = QImage(800, 600, QImage.Format_ARGB32)
        self.pixmap.fill(Qt.transparent)

        self.options = self.parent_display.controller.get_options()
        self.preview_position = None
        self.init_tools()

    def init_tools(self):
        self.tools = [
            FreehandDraw(self, DrawTool.ADD, Qt.LeftButton),
            FreehandEraser(self, DrawTool.SUBTRACT, Qt.LeftButton),
            RectInserter(self, DrawTool.RECT_ADD, Qt.LeftButton),
            RectDrag(self, DrawTool.RECT_DRAG, Qt.LeftButton),
            CircleInserter(self, DrawTool.CIRCLE_ADD, Qt.LeftButton),
            CircleDrag(self, DrawTool.CIRCLE_DRAG, Qt.LeftButton),
            PathTool(self, DrawTool.PATH_DRAW, Qt.LeftButton),
            PolygonTool(self, DrawTool.POLYGON_DRAW, Qt.LeftButton, Qt.RightButton),
            GridRectDraw(self, DrawTool.GRID_RECT_ADD, Qt.LeftButton),
            GridRectErase(self, DrawTool.GRID_RECT_SUBTRACT, Qt.LeftButton)
        ]

    def register_grid(self, grid_canvas):
        self.grid_canvas = grid_canvas
        

    def get_tool(self):
        return self.parent_display.controller.current_tool
    
    def mousePressEvent(self, event: QMouseEvent):
        for tool in self.tools:
            if tool.associated_tool == self.get_tool() and event.button() == tool.draw_button:
                tool.mouse_press(event)
                return
            if tool.associated_tool == self.get_tool() and event.button() == tool.secondary_button:
                tool.secondary_press(event)
                return

    def mouseMoveEvent(self, event: QMouseEvent):
        # Update the cursor position for the preview
        self.preview_position = event.pos()
        self.parent_display.update()
        for tool in self.tools:
            if tool.associated_tool == self.get_tool():
                tool.mouse_move(event)
                return


    def mouseReleaseEvent(self, event: QMouseEvent):
        for tool in self.tools:
            if tool.associated_tool == self.get_tool() and event.button() == tool.draw_button:
                tool.mouse_release(event)
                return

    def paint(self, painter):
        if not self.preview_position:
            return 
        for tool in self.tools:
            if tool.associated_tool == self.get_tool():
                tool.paint(painter)
                return


    def update_options(self):
        self.options = self.parent_display.controller.get_options()
        
        for tool in self.tools:
            if tool.associated_tool == self.get_tool():
                tool.update_options(self.options)

  