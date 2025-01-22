

class Tool():

    def __init__(self, canvas, associated_tool, draw_button):
        self.canvas = canvas
        self.associated_tool = associated_tool
        self.draw_button = draw_button

    def mouse_press(self, event):
        pass
    
    def mouse_release(self, event):
        pass

    def mouse_move(self, event):
        pass

    def paint(self, painter):
        pass

    def update_options(self, options):
        pass
