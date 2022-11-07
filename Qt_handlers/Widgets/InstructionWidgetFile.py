from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

class InstructionWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(r'Qt_handlers\ui_files\instruction_widget.ui', self)
        self.initUI()
    
    def initUI(self):
        pass