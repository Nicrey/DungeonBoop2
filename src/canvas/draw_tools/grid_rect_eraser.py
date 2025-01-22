

from canvas.draw_tools.abstract_tool import Tool
from PySide6.QtWidgets import ( QWidget)
from PySide6.QtGui import QPainter, QPixmap, QPen, QBrush, QMouseEvent, QImage, QColor
from PySide6.QtCore import Qt, QPoint, QRect

from canvas.draw_tools.utils.grid_utils import get_grid_start, get_grid_tile, grid_draw_useful

class GridRectErase(Tool):
    erasing = False
    grid_size = 32 
    last_grid_x = None
    last_grid_y = None

    def mouse_press(self, event):
        self.erasing = True

    def mouse_release(self, event):
        self.try_erase_grid_rect(event)

        self.last_grid_x = None
        self.last_grid_y = None
        self.erasing = False
        self.canvas.parent_display.canvas_changes()

    def mouse_move(self, event):
        self.try_erase_grid_rect(event)

    def update_options(self, options):
        self.grid_size = options[0].current_size
        self.canvas.grid_canvas.update_grid(self.grid_size)
        self.last_grid_x = None
        self.last_grid_y = None


    ###############
    # Basic Drawing
    ###############
    
    def try_erase_grid_rect(self, event):
        if self.erasing and grid_draw_useful(self,event.pos()):
            self.draw_grid_rect(get_grid_start(event.pos().x(), event.pos().y(), self.canvas.grid_canvas.grid_start, self.grid_size), self.grid_size)
            self.last_grid_x, self.last_grid_y = get_grid_tile(event.pos().x(), event.pos().y(), self.grid_size)
            
    def draw_grid_rect(self, position, size):
        painter = QPainter(self.canvas.pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_Clear)  
        rect_top_left = position
        rect = QRect(rect_top_left.x(), rect_top_left.y(),size, size)
        painter.fillRect(rect, QColor(0, 0, 0, 0))  
        painter.end()
