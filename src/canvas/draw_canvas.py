from PySide6.QtWidgets import ( QWidget)
from PySide6.QtGui import QPainter, QPixmap, QPen, QBrush, QMouseEvent, QImage, QColor
from PySide6.QtCore import Qt, QPoint, QRect


from canvas.draw_tools.circle_drag import CircleDrag
from canvas.draw_tools.circle_inserter import CircleInserter
from canvas.draw_tools.freehand_draw import FreehandDraw
from canvas.draw_tools.freehand_erase import FreehandEraser
from canvas.draw_tools.grid_rect_drawer import GridRectDraw
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
        self.tools = {
            DrawTool.ADD: FreehandDraw(self, Qt.LeftButton),
            DrawTool.SUBTRACT: FreehandEraser(self, Qt.LeftButton),
            DrawTool.RECT_ADD: RectInserter(self, Qt.LeftButton),
            DrawTool.RECT_DRAG: RectDrag(self, Qt.LeftButton),
            DrawTool.CIRCLE_ADD: CircleInserter(self, Qt.LeftButton),
            DrawTool.CIRCLE_DRAG: CircleDrag(self, Qt.LeftButton),
            DrawTool.PATH_DRAW: PathTool(self, Qt.LeftButton),
            DrawTool.POLYGON_DRAW: PolygonTool(self, Qt.LeftButton, Qt.RightButton),
            DrawTool.GRID_RECT_ADD: GridRectDraw(self, Qt.LeftButton, Qt.RightButton)
        }

    def register_grid(self, grid_canvas):
        self.grid_canvas = grid_canvas
        

    def get_tool(self):
        return self.parent_display.controller.current_tool
    
    def mousePressEvent(self, event: QMouseEvent):
        tool = self.tools[self.get_tool()]
        if event.button() == tool.draw_button:
            tool.mouse_press(event)
            return
        if event.button() == tool.secondary_button:
            tool.secondary_press(event)
            return

    def mouseMoveEvent(self, event: QMouseEvent):
        # Update the cursor position for the preview
        self.preview_position = event.pos()
        self.parent_display.update()
        tool = self.tools[self.get_tool()]
        tool.mouse_move(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        tool = self.tools[self.get_tool()]
        if event.button() == tool.draw_button:
            tool.mouse_release(event)
            return
        if event.button() == tool.secondary_button:
            tool.secondary_release(event)
            return

    def paint(self, painter):
        if not self.preview_position:
            return 
        tool = self.tools[self.get_tool()]
        tool.paint(painter)


    def update_options(self):
        self.options = self.parent_display.controller.get_options()
        tool = self.tools[self.get_tool()]
        tool.update_options(self.options)

  