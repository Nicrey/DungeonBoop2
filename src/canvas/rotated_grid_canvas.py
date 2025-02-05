import math
from PySide6.QtWidgets import ( QWidget)
from PySide6.QtGui import  QImage, QPainter
from PySide6.QtCore import Qt, QPoint

from canvas.draw_tools.utils.grid_utils import rotate_point
import config



class RotatedGridCanvas(QWidget):
        
    def __init__(self, parent_display=None, draw_canvas=None):
        super().__init__()
        self.parent_display = parent_display  

        self.width = 800
        self.height = 600
        
        # Initialize the drawing surface
        self.pixmap = QImage(config.WIDTH, config.HEIGHT, QImage.Format_ARGB32)
        self.pixmap.fill(Qt.transparent)

        self.grid_start = {}
        self.draw_canvas = draw_canvas
        self.draw_canvas.register_grid(self)
        self.update_grid(32, 0)
        

    def update_grid(self, grid_size, grid_angle):
        dx = 0
        dy = 0
        grid_points = []
        self.grid_start = {}
        while (dx < self.width*2):
            dy = -self.height*2 - ((-self.height*2) % grid_size)
            while(dy < self.height):
                x,y= rotate_point(dx,dy, -grid_angle)
                point = QPoint(x,y)
                if point.x() < 0 - grid_size or point.y() < 0 -grid_size or point.x() > self.width + grid_size or point.y() > self.height + grid_size:
                    dy += grid_size
                    continue
                self.grid_start[(dx//grid_size, dy//grid_size)] = QPoint(dx,dy)
                grid_points.append(point)
                dy += grid_size
            dx += grid_size
        self.paint_grid(grid_points)

        
    def paint_grid(self, grid_points):
        self.pixmap = QImage(config.WIDTH, config.HEIGHT, QImage.Format_ARGB32)
        self.pixmap.fill(Qt.transparent)
        painter = QPainter(self.pixmap)
        painter.setPen(Qt.black)
        for point in grid_points:
            painter.drawPoint(point)
