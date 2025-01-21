from typing import List
from PySide6.QtWidgets import (
    QSlider,QPushButton, QLabel, QLineEdit
)
from PySide6.QtGui import QPixmap,QIcon
from PySide6.QtCore import Qt   

# Tool options for third layer toolbar
# For Sizes in general
class SizeOption:
    current_size: int = 16
    name: str

    def __init__(self,name, controller):
        self.name = name
        self.controller = controller
        self.widgets = []

    def init_widgets(self):
        label = QLabel(self.name)
        slider = QSlider(Qt.Horizontal)
        slider.setRange(1, 50)
        slider.setValue(self.current_size)
        slider.setFixedWidth(150) 
        size_label = QLabel(str(self.current_size))
        slider.valueChanged.connect(self.direct_update)
        # Add widgets to the toolbar
        self.widgets = [label, slider, size_label]

    def direct_update(self, new_size):
        self.current_size = new_size
        self.widgets[2].setText(str(self.current_size))
        self.controller.options_update()

    def increase(self, how_much=16):
        self.current_size += how_much
        self.controller.options_update()
    
    def get_widgets(self):
        self.init_widgets()
        return self.widgets

# For Icon Tools
class Icon:
    path: str = ""
    def __init__(self, path):
        self.path = path

class IconSelectOption:
    icon_list: List[Icon] = []
    selected_idx: int = 0

    def __init__(self,name, controller):
        self.name = name
        self.controller = controller
        self.icon_list = [
            Icon("../resources/icons/down.png"),
            Icon("../resources/icons/up.png")
        ]
        self.widgets = []

    def get_icon(self):
        return QPixmap(self.icon_list[self.selected_idx].path)

    def select_icon(self, new_idx):
        self.selected_idx = new_idx
        for i,btn in enumerate(self.widgets):
            if i == new_idx:
                btn.setStyleSheet("border: 2px solid blue;")
            else:
                btn.setStyleSheet("")
        self.controller.options_update()

    def init_widgets(self):
        self.widgets = []
        for i,icon in enumerate(self.icon_list):
            button = QPushButton()
            button.setIcon(QIcon(icon.path))
            button.setFixedSize(25, 25)
            button.clicked.connect(lambda checked, idx=i: self.select_icon(idx))
            self.widgets.append(button)
        self.select_icon(0)


    def get_widgets(self):
        self.init_widgets()
        return self.widgets

# For Text Tools
class FontSelectOption:
    font_list: List[str] = []
    selected_idx: int = 0

    def __init__(self,name, controller):
        self.name = name
        self.controller = controller

    def get_font(self):
        return self.font_list[self.selected_idx]

    def select_font(self, new_idx):
        self.selected_idx = new_idx
        self.controller.options_update()
    
    def get_widgets(self):
        widgets = []
        return widgets

class TextOption:
    text: str = ""

    def __init__(self, name, controller):
        self.name = name
        self.controller = controller 

    def set_text(self):
        self.text = self.text_input.text()
        self.controller.options_update()
    
    def init_widgets(self):
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Text eingeben") 
        self.text_input.textEdited.connect(self.set_text)
        self.widgets = [self.text_input]

    def get_widgets(self):
        self.init_widgets()
        return self.widgets