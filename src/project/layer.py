from canvas.abstract_canvas import AbstractCanvas
from PySide6.QtGui import QPainter, QImage, QPixmap
from PySide6.QtCore import Qt

from canvas.border_canvas import BorderCanvas
from canvas.draw_canvas import DrawCanvas
from canvas.grid_canvas import GridCanvas
from canvas.icon_canvas import IconCanvas
from canvas.rotated_grid_canvas import RotatedGridCanvas
from canvas.text_canvas import TextCanvas

class Layer:

    def __init__(self, name, controller):
        self.name = name

        self.draw_canvas = DrawCanvas(parent_display=controller.canvas_controller)
        self.icon_canvas = IconCanvas(parent_display=controller.canvas_controller)
        self.text_canvas = TextCanvas(parent_display=controller.canvas_controller)
        self.border_canvas = BorderCanvas(parent_display=controller.canvas_controller, draw_canvas=self.draw_canvas)
        self.grid_canvas = RotatedGridCanvas(parent_display=controller.canvas_controller, draw_canvas=self.draw_canvas)


    def get_canvases(self):
        return [
            self.draw_canvas,
            self.icon_canvas,
            self.text_canvas,
            self.border_canvas,
            self.grid_canvas
        ]
    
    def set_canvases(self, canvas_list):
        self.draw_canvas = canvas_list[0]
        self.icon_canvas = canvas_list[1]
        self.text_canvas = canvas_list[2]
        self.border_canvas = canvas_list[3]
        self.grid_canvas = canvas_list[4]

    def get_preview_image(self):
        return self.get_combined_image(preview=True)
    
    def get_combined_image(self, preview = False):
        image_x = 800 if not preview else 400
        image_y = 600 if not preview else 250
        combined = QImage(image_x, image_y, QImage.Format_ARGB32)
        combined.fill(Qt.white)
        painter = QPainter(combined)
        painter.drawImage(0, 0, self.draw_canvas.pixmap.scaled(image_x, image_y))
        painter.drawImage(0, 0, self.icon_canvas.pixmap.scaled(image_x, image_y))
        painter.drawImage(0, 0, self.text_canvas.pixmap.scaled(image_x, image_y))
        painter.drawImage(0, 0, self.border_canvas.pixmap.scaled(image_x, image_y))
        painter.end()
        return QPixmap.fromImage(combined)