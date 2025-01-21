from PySide6.QtWidgets import QToolBar
from PySide6.QtGui import QAction, QIcon

from ui.toolbars.layer_tool import LayerToolOptions
from ui.toolbars.tools import Mode, get_tools


def setup_toolbar(controller):
    # Toolbar
    toolbar = QToolBar("Tools")
    tools = get_tools(controller.mode)

    for tool in tools:
        action = QAction(QIcon(), tool.value, controller)
        action.triggered.connect(lambda checked=False, t=tool: controller.set_tool(t))
        toolbar.addAction(action)
    return toolbar

def setup_modebar(controller):
    modebar = QToolBar("Modes")
    for mode in Mode:
        action = QAction(QIcon(), mode.value, controller)
        action.triggered.connect(lambda checked=False, t=mode: controller.set_mode(t))
        modebar.addAction(action)
    return modebar

def setup_third_layer_toolbar(controller):
    third_layer_tools = controller.get_options()
    option_bar = QToolBar("Tool Options")
    for option in third_layer_tools:
        for widget in option.get_widgets():
            option_bar.addWidget(widget)
    option_bar.setStyleSheet("""
        QToolBar {
            background-color: #f5f5f5;
            border: 1px solid #ccc;
        }
        QLabel {
            font-size: 12px;
            margin-right: 10px;
        }
        QSlider {
            margin-right: 10px;
        }
    """)
    return option_bar
        
def setup_layer_toolbar(controller):
    layer_bar = QToolBar("Layers")
    options = LayerToolOptions(controller)
    for widget in options.get_widgets():
        try:
            layer_bar.addWidget(widget)
        except TypeError:
            layer_bar.addAction(widget)
    return layer_bar

def highlight_action(highlight_action_text, toolbar):
    for action in toolbar.actions():
        widget =toolbar.widgetForAction(action)
        widget.setStyleSheet("")
        if action.text() == highlight_action_text:
            widget.setStyleSheet("background-color: lightblue; color: black;")