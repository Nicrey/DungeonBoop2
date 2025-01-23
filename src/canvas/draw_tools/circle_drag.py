from canvas.draw_tools.abstract_tool import Tool
from canvas.draw_tools.utils.draw_utils import draw_circle_2points


class CircleDrag(Tool):

    start_pos = None
    circle = False
    by_midpoint = True

    def mouse_press(self, event):
        self.start_pos = event.pos()

    def mouse_release(self, event):
        draw_circle_2points(self.canvas,
                            self.start_pos,
                            event.pos(),
                            true_circle=self.circle,
                            by_midpoint=self.by_midpoint)
        self.canvas.parent_display.canvas_changes()
        self.start_pos = None

    def paint(self, painter):
        if self.start_pos:
            painter.setOpacity(0.5)
            draw_circle_2points(self.canvas,
                                self.start_pos,
                                self.canvas.preview_position,
                                True,
                                painter=painter,
                                true_circle=self.circle,
                                by_midpoint=self.by_midpoint)
            painter.setOpacity(1.0)

    def update_options(self, options):
        self.circle = options[0].checked
        self.by_midpoint = options[1].checked
