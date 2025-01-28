import sys
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QHBoxLayout,
                               QInputDialog, QLineEdit, QMainWindow, QVBoxLayout, QWidget)

from canvas.canvas_controller import CanvasController
from file_handler import save_project
from project.project import Project
from ui.layer_preview import LayerPreview
from ui.menu_bar import FileMenu
from ui.shortcuts import init_shortcuts
from ui.toolbars.tool_options import (CheckboxOption, ColorOption, FontSelectOption, IconSelectOption, LimitedSliderOption,
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
        self.canvas_controller = CanvasController(self)

        init_shortcuts(self)
        self.mode = Mode.DRAW
        self.current_tool = DrawTool.ADD
        self.setup_tool_option_map()
        

        # Project
        self.project = Project()
        self.project.new_layer(self)
        
        self.canvas_controller.update_layer()
        
        # Toolbars
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
            DrawTool.ADD : [SizeOption("Brush Size", self, 16, 4, 200)],
            DrawTool.SUBTRACT: [SizeOption("Eraser Size", self, 16, 4, 200)],
            DrawTool.RECT_ADD: [SizeOption("X",self, 50, 5, 200), SizeOption("Y",self, 50, 5, 200)],
            DrawTool.RECT_DRAG: [CheckboxOption("Square", self), CheckboxOption("By Midpoint", self)],
            DrawTool.CIRCLE_ADD: [SizeOption("X",self, 50, 5, 200), SizeOption("Y",self, 50, 5, 200)],
            DrawTool.CIRCLE_DRAG: [CheckboxOption("Circle", self),CheckboxOption("By Midpoint", self)],
            DrawTool.PATH_DRAW: [SizeOption("Path Width", self, 10, 5, 100), CheckboxOption("Snap", self)],
            DrawTool.POLYGON_DRAW: [CheckboxOption("Snap", self)],
            DrawTool.GRID_RECT_ADD: [LimitedSliderOption("Grid Size", self, values=[8,16,24,32,40,48,56,64], default=3), LimitedSliderOption("Grid Rotation", self, values=[0,15,30,45,60,75,90])],
            IconTool.ADD_ICON: [SizeOption("Size",self, 25, 5, 50), LimitedSliderOption("Rotation", self, values=[0,15,30,45,60,75,90]), ColorOption("Tint", self), IconSelectOption("Icon",self)],
            IconTool.REMOVE_ICON: [SizeOption("Size", self, 16, 4, 200)],
            TextTool.ADD_TEXT: [SizeOption("FontSize",self, 16, 4, 200), ColorOption("Color", self),FontSelectOption("Font",self), TextOption("Text", self)],
            TextTool.REMOVE_TEXT: [SizeOption("Size", self, 16, 4, 200)]
        }
    
    def get_options(self):
        return self.THIRD_LAYER_TOOL_MAP.get(self.current_tool, [])

    def undo(self):
        self.canvas_controller.canvas_history.undo()
    
    def save_project(self):
        save_project(controller=self, p=self.project)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
