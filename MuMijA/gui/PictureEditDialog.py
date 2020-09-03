from PySide2.QtWidgets import QDialog,QVBoxLayout
from PySide2.QtGui import QIcon
from gui.PictureEditWindow import PictureEditWindow

class PictureEditDialog(QDialog):
    """
    Dijalog za editovanje slike

    Attributes:
        object: slika koja se edituje
    """

    def __init__(self, object):
        """
        Konstruktor

        Args:
            object(Picture): slika koja se edituje
        """
        super(PictureEditDialog, self).__init__()
        self.object = object
        mainWindow = PictureEditWindow(self.object)
        self.setModal(True)
        tmpLayout = QVBoxLayout()
        tmpLayout.addWidget(mainWindow)
        self.setLayout(tmpLayout)
        self.setWindowTitle("Picture Editor")
        self.setFixedHeight(600)
        self.setFixedWidth(800)
        self.setWindowIcon(QIcon("src/PictureEdit_menu.png"))