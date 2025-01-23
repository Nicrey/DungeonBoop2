

from canvas.draw_tools.abstract_tool import Tool
from canvas.draw_tools.utils.draw_utils import draw_rect, get_rect



class FreehandDraw(Tool):

    drawing = False
    draw_size = 32 

    def mouse_press(self, event):
        self.drawing = True

    def mouse_release(self, event):
        self.drawing = False
        self.canvas.parent_display.canvas_changes()

    def mouse_move(self, event):
        if self.drawing:
            rect = get_rect(event.pos(), self.draw_size)
            draw_rect(self.canvas, rect)

    def paint(self, painter):
        painter.setOpacity(0.5)
        rect = get_rect(self.canvas.preview_position, self.draw_size)
        draw_rect(self.canvas, rect, preview=True, painter=painter)
        painter.setOpacity(1.0)

    def update_options(self, options):
        self.draw_size = options[0].current_size
