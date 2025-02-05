import numpy as np
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPixmap, QMouseEvent, QImage, QColor
from PySide6.QtCore import Qt, QPoint, QRect
from scipy.ndimage import convolve

import config
from ui.toolbars.tools import DrawTool
from scipy.ndimage import binary_dilation

class BorderCanvas(QWidget):

    def __init__(self, parent_display=None, draw_canvas=None):
        super().__init__()
        self.drawing = False
        self.last_point = QPoint()
        self.parent_display = parent_display  # Reference to CanvasController

        # Initialize the drawing surface
        self.pixmap = QImage(config.WIDTH, config.HEIGHT, QImage.Format_ARGB32)
        self.pixmap.fill(Qt.transparent)
        self.draw_canvas = draw_canvas


    def blacken_near_transparent(self):
        """
        Blacken pixels in this canvas's pixmap based on transparency in another pixmap.
        """
        """
        Blacken pixels in this canvas's pixmap based on transparency in another pixmap.
        Optimized with numpy for speed.
        """
        self.pixmap = QImage(config.WIDTH, config.HEIGHT, QImage.Format_ARGB32)
        self.pixmap.fill(Qt.transparent)
        source_image = self.draw_canvas.pixmap
        source_width, source_height = source_image.width(), source_image.height()

        # Convert source image to numpy array
        source_bits = source_image.bits()
        source_array = np.frombuffer(source_bits, dtype=np.uint8).reshape((source_height, source_width, 4))

        # Find transparency in the source image
        alpha_channel = source_array[:, :, 3]  # Extract the alpha channel
        is_transparent = alpha_channel == 0

        # Create a square mask of size 6x6 for dilation
        square_kernel = np.ones((6, 6), dtype=bool)

        # Dilate the transparent pixels using the kernel
        neighbor_mask = binary_dilation(is_transparent, structure=square_kernel)

        # Combine the neighbor mask with non-transparent pixels
        to_blacken = neighbor_mask & (alpha_channel > 0)

        # Apply the blacken operation
        target_image = self.pixmap
        target_bits = target_image.bits()
        target_array = np.frombuffer(target_bits, dtype=np.uint8).reshape((source_height, source_width, 4))

        target_array[to_blacken] = [0, 0, 0, 255]  # Black color with full opacity

        # Update the pixmap
        self.pixmap = target_image

    def paint(self, painter):
        pass