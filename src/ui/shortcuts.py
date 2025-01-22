
from PySide6.QtGui import QKeySequence, QShortcut

def init_shortcuts(controller):
    controller.undo_shortcut = QShortcut(QKeySequence("Ctrl+Z"), controller)
    controller.undo_shortcut.activated.connect(controller.undo)