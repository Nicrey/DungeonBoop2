from PySide6.QtWidgets import (
    QListView, QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt, QSize

class LayerPreview(QListWidget):

    def __init__(self, controller):
        super().__init__()
        self.setFixedWidth(185)
        self.setViewMode(QListView.IconMode)
        self.setIconSize(QSize(150, 100))
        self.setSpacing(10) 
        self.setDragDropMode(QListWidget.NoDragDrop)
        self.itemClicked.connect(self.change_layer)
        self.controller = controller
        self.update_list()

    def update_list(self):
        self.clear()
        for i, layer in enumerate(self.controller.project.layers):
            item = QListWidgetItem(f"{layer.name}")

            item.setIcon(layer.get_preview_image()) 
            if layer == self.controller.get_current_layer():
                item.setBackground(Qt.lightGray)

            self.addItem(item)
        
    def change_layer(self, item):
        index = self.row(item)
        self.controller.switch_layer(index)
