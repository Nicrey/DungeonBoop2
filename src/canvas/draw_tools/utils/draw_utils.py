import math
from PySide6.QtWidgets import ( QWidget)
from PySide6.QtGui import QPainter, QPixmap, QPen, QBrush, QMouseEvent, QImage, QColor
from PySide6.QtCore import Qt, QPoint, QRect


##############################
#   Misc Utils
############################


def snap_to_angle(pos1, pos2):
    """
    Snaps a position to the next 15 degree angle
    """
    dx = pos2.x() - pos1.x()
    dy = pos2.y() - pos1.y()
    dist = math.sqrt(dx*dx + dy*dy)
    angle = math.atan2(dy, dx)
    angle = round(angle / (math.pi / 16)) * (math.pi / 16)
    return pos1 + QPoint(round(math.cos(angle) * dist), round(math.sin(angle) * dist))

def prepare_painter(preview, painter, canvas=None):
    if not painter:
        painter = QPainter(canvas.pixmap)
    if preview:
        pen = QPen(QColor(0,0,0,255))
        pen.setWidth(2)
        painter.setPen(pen)
    else:
        pen = QPen(QColor(0,0,0,0))
        pen.setWidth(1)
        painter.setPen(pen)
    return painter

def normal_draw_brush(painter):
    brush = QBrush(QColor(230,230,230,255))
    painter.setBrush(brush)
    return painter

def get_sizes_by_2pos(position_1, position_2, symmetric):
    size_x  = position_2.x() - position_1.x()
    size_y = position_2.y() - position_1.y()
    if symmetric:
        size_x = min(abs(size_x), abs(size_y))
        size_y = size_x
        size_x = -size_x if position_2.x() < position_1.x() else size_x
        size_y = -size_y if position_2.y() < position_1.y() else size_y
    return size_x,size_y

def get_rect(position, size_x, size_y=None, by_midpoint=True):
    """
    Creates a rect based on a position and two sizes.
    Either considers the position the top left corner or the midpoint
    """
    size_y = size_x if size_y is None else size_y
    if by_midpoint:
        rect_top_left = position - QPoint(size_x // 2, size_y // 2)
    else:
        rect_top_left = position
    rect = QRect(rect_top_left.x(), rect_top_left.y(),size_x, size_y)
    return rect
    
#############################
#    RECTANGLE
################################

def draw_rect(
        canvas,
        rect,
        preview=False,
        painter=None,
    ):
    painter = prepare_painter(preview, painter, canvas)
    painter = normal_draw_brush(painter)
    painter.drawRect(rect)  
    if not preview:
        painter.end()


def draw_rect_2points(canvas, position_1, position_2, preview=False, painter=None, square=False, by_midpoint=False):
    size_x, size_y = get_sizes_by_2pos(position_1, position_2, square)
    rect = get_rect(position_1, size_x, size_y, by_midpoint)
    draw_rect(canvas,rect, preview, painter)


######################
#       CIRCLE
#####################

def draw_circle(
        canvas,
        rect,
        preview=False,
        painter=None
    ):
    painter = prepare_painter(preview, painter, canvas)
    painter = normal_draw_brush(painter)
    painter.drawEllipse(rect)  
    if not preview:
        painter.end()


def draw_circle_2points(
        canvas,
        position_1,
        position_2,
        preview=False,
        painter=None,
        true_circle=False, by_midpoint=False):
    size_x, size_y = get_sizes_by_2pos(position_1, position_2, true_circle)
    rect = get_rect(position_1, size_x, size_y, by_midpoint)
    draw_circle(canvas, rect, preview, painter)

