from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt

class CustomTitleBar(QWidget):
    """Benutzerdefinierte Titelleiste für ein modernes Aussehen"""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        
        self.title = QLabel(self.parent.windowTitle())
        self.title.setAlignment(Qt.AlignCenter)
        
        self.minimize_button = QPushButton("_")
        self.maximize_button = QPushButton("🗖")
        self.close_button = QPushButton("X")
        
        self.minimize_button.setFixedSize(40, 30)
        self.maximize_button.setFixedSize(40, 30)
        self.close_button.setFixedSize(40, 30)
        
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.minimize_button)
        self.layout.addWidget(self.maximize_button)
        self.layout.addWidget(self.close_button)
        
        self.setLayout(self.layout)
        
        self.minimize_button.clicked.connect(self.parent.showMinimized)
        self.maximize_button.clicked.connect(self.toggle_maximize)
        self.close_button.clicked.connect(self.parent.close)
        
        self.start_move_pos = None

    def toggle_maximize(self):
        """Wechselt zwischen maximiertem und normalem Fensterzustand"""
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()

    def mouseDoubleClickEvent(self, event):
        """Maximiert das Fenster bei Doppelklick"""
        self.toggle_maximize()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_move_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.start_move_pos:
            delta = event.globalPos() - self.start_move_pos
            self.parent.move(self.parent.pos() + delta)
            self.start_move_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.start_move_pos = None
