

import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMenuBar, QFileDialog, QMessageBox, QVBoxLayout, QWidget
)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt
import sys


from canvas.abstract_canvas import AbstractCanvas
from canvas.border_canvas import BorderCanvas
from canvas.draw_canvas import DrawCanvas
from canvas.grid_canvas import GridCanvas
from canvas.icon_canvas import IconCanvas
from canvas.rotated_grid_canvas import RotatedGridCanvas
from canvas.text_canvas import TextCanvas
from project.project import Layer, Project

def save_project_as(p: Project, controller):
    """Saves the project to disc imploring a filedialog first"""
    selected_path = QFileDialog.getExistingDirectory(controller, "Select Project Save Location")
    if selected_path:
        p.save_path = selected_path
        save_project(p, controller)
    
    

def save_project(p: Project, controller):
    """Saves the project to disc"""
    if not p.save_path:
        save_project_as(p, controller)
    # Create main project folder if not exists
    main_folder = os.path.join(p.save_path , p.name)
    os.makedirs(main_folder, exist_ok=True)
    final_folder = os.path.join(main_folder, "finals")
    os.makedirs(final_folder, exist_ok=True)
    # Create rendered image folder
    for layer in p.layers:
        layer_folder = os.path.join(main_folder, layer.name)
        os.makedirs(layer_folder, exist_ok=True)
        save_layer(layer, layer_folder)
        save_rendered_image(layer, final_folder)

def save_layer(l: Layer, layer_folder_path):
    """
    Saves the layer data to disc, so that it can be 
    opened as three separate layers
    """
    # Create layer folder
    
    for i, canvas in enumerate(l.get_canvases()):
        canvas_filename = os.path.join(layer_folder_path, f"{l.name}_{i}.png")
        canvas.pixmap.save(canvas_filename)

def save_rendered_image(l: Layer, final_folder):
    """
    Saves a rendered image of all three layers on top
    of each other that can be used
    """
    filename = os.path.join(final_folder, f"{l.name}.png")
    pixmap = l.get_combined_image()
    pixmap.save(filename)

def open_project(controller) -> Project:
    """Opens a project from disc"""
    folder_path = QFileDialog.getExistingDirectory(controller, "Select Project Folder")
    if folder_path:
        try:
            open_project_by_path(folder_path, controller)
        except Exception as e:
            QMessageBox.critical(controller, "Error", f"Failed to load project: {str(e)}")

def open_project_by_path(project_path, controller):
    if not os.path.exists(project_path):
        raise FileNotFoundError(f"Project path '{project_path}' does not exist.")

    # Load project name from the folder name
    project_name = os.path.basename(project_path)

    # Initialize the Project
    project = Project(name=project_name, save_path=project_path)
    layers = []
    # Iterate through the layer folders (excluding the "finals" folder)
    for dir in os.listdir(project_path):
        layer_path = os.path.join(project_path, dir)
        if os.path.isdir(layer_path) and dir != "finals":
            # Create a new Layer object
            layer = Layer(name=dir, controller=controller)

            # Load canvases for this layer
            canvases = []
            draw_canvas = None
            for i, canvas_file in enumerate(sorted(os.listdir(layer_path))):
                if canvas_file.endswith(".png"):
                    canvas_path = os.path.join(layer_path, canvas_file)

                    # Create a QPixmap from the file
                    pixmap = QImage(canvas_path)

                    # Create a Canvas object (assuming you have a Canvas class)
                    if i == 0:
                        canvas = DrawCanvas(parent_display=controller.canvas_controller)
                        draw_canvas = canvas
                    if i == 1:
                        canvas = IconCanvas(parent_display=controller.canvas_controller)
                    if i == 2:
                        canvas = TextCanvas(parent_display=controller.canvas_controller)
                    if i == 3:
                        canvas = BorderCanvas(parent_display=controller.canvas_controller, draw_canvas=draw_canvas)
                    if i == 4:
                        canvas = RotatedGridCanvas(parent_display=controller.canvas_controller, draw_canvas=draw_canvas)
                    canvas.pixmap = pixmap
                    canvases.append(canvas)
            
            # Set canvases to the layer
            layer.set_canvases(canvases)

            # Add the layer to the project
            layers.append(layer)
    project.layers = layers
    controller.project = project
    controller.layer_update()