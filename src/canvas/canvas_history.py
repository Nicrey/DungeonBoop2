

from ui.toolbars.tools import Mode
from PySide6.QtGui import QImage


class CanvasHistory:

    def __init__(self, controller, canvas_controller):
        self.controller = controller
        self.canvas_controller = canvas_controller  
        self.draw_history = []
        self.icon_history = []
        self.text_history = []
        self.last_change = None

    def trigger(self):
        history = self.get_history()
        if len(history) > 50:
            history.pop(0)
        canvas = self.canvas_controller.canvases[self.canvas_controller.active_canvas_idx()]
        history.append(canvas.pixmap.copy())

    def trigger_all(self):
        histories = [self.draw_history, self.icon_history, self.text_history]
        for i, (canvas, history) in enumerate(zip(self.canvas_controller.canvases, histories)):
            if i == 3:
                break
            history.append(canvas.pixmap.copy())

    def undo(self):
        canvas_idx = self.canvas_controller.active_canvas_idx()
        history_to_undo = self.get_history()
        if len(history_to_undo) <= 1:
            return
        history_to_undo.pop()
        self.canvas_controller.canvases[canvas_idx].pixmap = history_to_undo[-1].copy()
        self.canvas_controller.undo_complete()
        
    def get_history(self):
        if self.controller.mode == Mode.DRAW:
            history_to_undo = self.draw_history
        elif self.controller.mode == Mode.ICON:
            history_to_undo = self.icon_history
        elif self.controller.mode == Mode.TEXT:
            history_to_undo = self.text_history
        else:
            return
        return history_to_undo
    
    def redo(self):
        pass
