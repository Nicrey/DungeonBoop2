from PySide6.QtGui import QAction, QIcon

from ui.toolbars.tools import LayerTool

class LayerToolOptions:

    def __init__(self, controller):
        self.controller = controller

    def get_widgets(self):
        self.widgets = []
        for tool in LayerTool:
            action = QAction(QIcon(), tool.value, self.controller)
            action.triggered.connect(lambda checked=False, t=tool: self.layer_action(t))
            self.widgets.append(action)
        return self.widgets
    
    def layer_action(self, action):
        self.controller.layer_action(action)
