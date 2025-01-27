

class Tool():

    def __init__(self, canvas, draw_button, secondary_button=None):
        self.canvas = canvas
        self.draw_button = draw_button
        self.secondary_button = secondary_button

    def mouse_press(self, event):
        pass
    
    def secondary_press(self, event):
        pass
    
    def mouse_release(self, event):
        pass
    
    def secondary_release(self, event):
        pass

    def mouse_move(self, event):
        pass

    def paint(self, painter):
        pass

    def update_options(self, options):
        pass
