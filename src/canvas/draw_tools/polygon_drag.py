

import math
from canvas.draw_tools.abstract_tool import Tool
from PySide6.QtGui import QPainter, QMouseEvent, QPen, QImage, QColor
from PySide6.QtCore import Qt, QPoint

from canvas.draw_tools.utils.draw_utils import dist, draw_circle, get_rect, normal_draw_brush, prepare_painter, snap_to_angle

class PolygonDragTool(Tool):

    start_pos = None
    erasing = False
    sides = 3
    
    def mouse_press(self, event):
        self.erasing = False
        self.start_pos = event.pos()
    
    def secondary_press(self, event):
        self.erasing = True
        self.start_pos = event.pos()

    def mouse_release(self, event):
        if self.start_pos:
            self.draw_polygon(event.pos())
            self.canvas.parent_display.canvas_changes()
            self.start_pos = None
            self.erasing = False
        
    def secondary_release(self, event):
        if self.start_pos:
            self.draw_polygon(event.pos())
            self.canvas.parent_display.canvas_changes()
            self.start_pos = None
            self.erasing = False

    def paint(self, painter):
        if self.start_pos:
            painter.setOpacity(0.5)
            self.draw_polygon(self.canvas.preview_position, True,painter)
            painter.setOpacity(1.0)

    def update_options(self, options):
        self.sides = options[0].current_size
        self.snap = options[1].checked


    def draw_polygon(self, current_pos, preview=False,painter=None):
        current_pos = snap_to_angle(self.start_pos, current_pos) if self.snap else current_pos
        painter = QPainter(self.canvas.pixmap) if not painter else painter
        painter = prepare_painter(preview, painter, self.canvas)
        painter = normal_draw_brush(painter, self.erasing if not preview else False)
        radius = dist(self.start_pos, current_pos)
        angle_step = 360 / self.sides
        points = [current_pos]  # Start with the current position as one corner
        start_angle = math.atan2(current_pos.y() - self.start_pos.y(), current_pos.x() - self.start_pos.x())
        for i in range(1, self.sides):
            angle = angle_step * i
            x = self.start_pos.x() + radius * math.cos(start_angle + math.radians(angle))
            y = self.start_pos.y() + radius * math.sin(start_angle + math.radians(angle))
            points.append(QPoint(x, y))

        painter.drawPolygon(points)
        if not preview:
            painter.end()
  
    