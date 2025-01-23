

from canvas.draw_tools.abstract_tool import Tool
from PySide6.QtGui import QPainter, QMouseEvent, QPen, QImage, QColor
from PySide6.QtCore import Qt, QPoint

from canvas.draw_tools.utils.draw_utils import normal_draw_brush, snap_to_angle

class PathTool(Tool):

    start = None
    width = 5
    snap = False
    
    def mouse_press(self, event):
        self.start = event.pos()
    
    def mouse_release(self, event):
        if self.snap:
            end_pos = snap_to_angle(self.start, event.pos())
        else:
            end_pos = event.pos()
        draw_line(self.start, end_pos, self.canvas, self.width)
        self.canvas.parent_display.canvas_changes()
        self.start = None

    def mouse_move(self, event):
        pass

    def paint(self, painter):
        if self.start:
            if self.snap:
                end_pos = snap_to_angle(self.start, self.canvas.preview_position)
            else:
                end_pos = self.canvas.preview_position
            draw_line(self.start, end_pos, self.canvas, self.width, painter=painter)

    def update_options(self, options):
        self.width = options[0].current_size
        self.snap = options[1].checked
        
def draw_line(start, end, canvas, width, painter=None):
    preview = True
    if not painter:
        painter = QPainter(canvas.pixmap)
        preview = False
    pen = QPen(QColor(230,230,230,255))
    pen.setWidth(width)
    painter.setPen(pen)
    painter = normal_draw_brush(painter)
    painter.drawLine(start, end)
    if not preview:
        painter.end()