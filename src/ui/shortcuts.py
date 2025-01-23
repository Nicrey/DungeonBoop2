
from PySide6.QtGui import QKeySequence, QShortcut

def init_shortcuts(controller):
    controller.undo_shortcut = QShortcut(QKeySequence("Ctrl+Z"), controller)
    controller.undo_shortcut.activated.connect(controller.undo)
    controller.save_shortcut = QShortcut(QKeySequence("Ctrl+S"), controller)
    controller.save_shortcut.activated.connect(controller.save_project)