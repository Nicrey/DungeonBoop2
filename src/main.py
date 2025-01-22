import sys
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QHBoxLayout,
                               QInputDialog, QLineEdit, QMainWindow, QVBoxLayout, QWidget)

from canvas.canvas_controller import CanvasController
from project.project import Project
from ui.layer_preview import LayerPreview
from ui.menu_bar import FileMenu
from ui.toolbars.tool_options import (FontSelectOption, IconSelectOption,
                                      SizeOption, TextOption)
from ui.toolbars.toolbar import (highlight_action, setup_layer_toolbar,
                                 setup_modebar, setup_third_layer_toolbar,
                                 setup_toolbar)
from ui.toolbars.tools import (DrawTool, IconTool, LayerTool, Mode, TextTool,
                               get_tools)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Paint App")
        self.setFixedSize(1000, 700)
        
        # MenuBar
        self.menu_bar = FileMenu(self)
        self.setMenuBar(self.menu_bar)

        # Toolbars
        self.mode = Mode.DRAW
        self.current_tool = DrawTool.ADD
        self.setup_tool_option_map()
        
        self.canvas_controller = CanvasController(self)

        # Project
        self.project = Project()
        self.project.new_layer(self)
        
        self.canvas_controller.update_layer()
        
        self.modebar = setup_modebar(self)
        self.addToolBar(Qt.TopToolBarArea, self.modebar)

        self.layer_bar = setup_layer_toolbar(self)
        self.addToolBar(Qt.TopToolBarArea, self.layer_bar)

        self.addToolBarBreak(Qt.TopToolBarArea)
        self.toolbar = setup_toolbar(self)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)
        self.options_bar = setup_third_layer_toolbar(self)
        self.addToolBar(Qt.TopToolBarArea, self.options_bar)

        # Status Bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Brush selected")

        self.set_mode(Mode.DRAW)

        # Layer preview
        self.layer_preview = LayerPreview(self)
        layer_preview_layout = QVBoxLayout()
        layer_preview_layout.addWidget(self.layer_preview)
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas_controller)

        main_layout = QHBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(layer_preview_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        self.layer_update()


    def set_tool(self, tool: Any):
        """Sets the current tool to use"""
        # self.canvas.set_tool(tool.value)
        self.current_tool = tool
        self.status_bar.showMessage(f"{tool.value} selected")
        highlight_action(tool.value, self.toolbar)

        self.removeToolBar(self.options_bar)
        self.options_bar = setup_third_layer_toolbar(self)
        self.addToolBar(Qt.TopToolBarArea, self.options_bar)
        self.options_update()
    
    def set_mode(self, mode: Mode):
        """Sets the current drawing mode, defaults to th
        e first tool of the mode to be selected"""
        self.removeToolBar(self.toolbar)
        self.mode = mode
        self.toolbar = setup_toolbar(self)
        self.addToolBarBreak(Qt.TopToolBarArea)
        self.addToolBar(Qt.TopToolBarArea,self.toolbar)
        highlight_action(mode.value, self.modebar)
        self.set_tool([x for x in get_tools(mode)][0])

    def get_current_layer(self):
        return self.project.get_current_layer()
    
    def layer_action(self, action: LayerTool):
        if action == LayerTool.GO_UP:
            self.project.switch_layer(next=True)
        if action == LayerTool.GO_DOWN:
            self.project.switch_layer(next=False)   
        if action == LayerTool.ADD_LAYER:
            self.project.new_layer(self)    
        if action == LayerTool.RENAME:
            self.rename_layer()
        self.layer_update()
    
    def rename_layer(self):
        current_layer = self.get_current_layer()
        new_name, ok = QInputDialog.getText(
            self,
            "Rename Layer",
            "Enter new name:",
            QLineEdit.Normal,
            current_layer.name,
        )
        if ok and new_name.strip():
            current_layer.name = new_name.strip()

    def switch_layer(self, index: int):
        self.project.switch_layer_to_specific(index)
        self.layer_update()
    
    def layer_update(self):
        self.canvas_controller.update_layer()  
        self.layer_preview.update_list()

    def options_update(self):
        self.canvas_controller.update_options()

    def setup_tool_option_map(self):
                # Third Layer tool map
        self.THIRD_LAYER_TOOL_MAP = {
            DrawTool.ADD : [SizeOption("Brush Size", self)],
            DrawTool.SUBTRACT: [SizeOption("Eraser Size", self)],
            DrawTool.RECT_ADD: [SizeOption("X",self), SizeOption("Y",self)],
            DrawTool.CIRCLE_ADD: [SizeOption("X",self), SizeOption("Y",self)],
            IconTool.ADD_ICON: [SizeOption("Size",self), IconSelectOption("Icon",self)],
            IconTool.REMOVE_ICON: [SizeOption("Size", self)],
            TextTool.ADD_TEXT: [SizeOption("FontSize",self), FontSelectOption("Font",self), TextOption("Text", self)],
            TextTool.REMOVE_TEXT: [SizeOption("Size", self)]
        }
    
    def get_options(self):
        return self.THIRD_LAYER_TOOL_MAP.get(self.current_tool, [])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
