from PySide2.QtWidgets import QDialog,QHBoxLayout
from PySide2.QtGui import QIcon
from gui.TextEditWindow import TextEditWindow

class TextEditDialog(QDialog):
    """
    Dijalog za editovanje text-a
    """

    def __init__(self, object):
        """
        Konstruktor

        Args:
            object(Text): text koji se edituje
        """
        super(TextEditDialog, self).__init__()
        mainWindow = TextEditWindow(object)
        self.setModal(True)
        tmpLayout = QHBoxLayout()
        tmpLayout.addWidget(mainWindow)
        self.setLayout(tmpLayout)
        self.setWindowTitle("Text Editor")
        self.setFixedHeight(400)
        self.setFixedWidth(600)
        self.setWindowIcon(QIcon("src/TextEdit_menu.png"))