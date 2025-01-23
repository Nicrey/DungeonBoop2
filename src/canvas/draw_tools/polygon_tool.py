

from canvas.draw_tools.abstract_tool import Tool
from PySide6.QtGui import QPainter, QMouseEvent, QPen, QImage, QColor
from PySide6.QtCore import Qt, QPoint

from canvas.draw_tools.utils.draw_utils import dist, draw_circle, get_rect, normal_draw_brush, prepare_painter, snap_to_angle

class PolygonTool(Tool):

    points = []
    snap = False
    
    def mouse_press(self, event):
        point = event.pos()
        if self.points:
            point = snap_to_angle(self.points[-1], event.pos()) if self.snap else event.pos()
            distance = dist(point, self.points[0])
            if distance < 10 and len(self.points) > 2:
                draw_poly(self.points, self.canvas)
                self.points = []
                self.canvas.parent_display.canvas_changes()
                return
        self.points.append(point)
    
    def secondary_press(self, event):
        self.points = []

    def paint(self, painter):
        if self.points:
            point = snap_to_angle(self.points[-1], self.canvas.preview_position) if self.snap else self.canvas.preview_position
            draw_poly(self.points + [point], self.canvas, True, painter)
            distance = dist(self.canvas.preview_position, self.points[0])
            if distance < 10 and len(self.points) > 2:
                rect = get_rect(self.canvas.preview_position, 10, 10, by_midpoint=True)
                draw_circle(self.canvas,rect,  True, painter)
            

    def update_options(self, options):
        self.points = []
        self.snap = options[0].checked
        
def draw_poly(points,  canvas, preview=False, painter=None):
    painter = prepare_painter(preview, painter, canvas)
    painter = normal_draw_brush(painter)
    painter.drawPolygon(points)
    if not preview:
        painter.end()