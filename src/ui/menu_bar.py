import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMenuBar, QFileDialog, QMessageBox, QVBoxLayout, QWidget
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import sys

from file_handler import open_project, save_project, save_project_as

class FileMenu(QMenuBar):
        
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        # File Menu
        file_menu = self.addMenu("File")

        # Save Action
        save_action = file_menu.addAction("Save")
        save_action.triggered.connect(self.save_project)

        # Save As Action
        save_as_action = file_menu.addAction("Save As")
        save_as_action.triggered.connect(self.save_project_as)

        open_action = file_menu.addAction("Open")
        open_action.triggered.connect(self.open_project)

    def save_project(self):
        save_project(self.controller.project, self.controller)

    def save_project_as(self):
        save_project_as(self.controller.project, self.controller)

    def open_project(self):
        open_project(self.controller)