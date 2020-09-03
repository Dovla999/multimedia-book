from PySide2.QtWidgets import QMainWindow, QVBoxLayout,QWidget,QAction,QFileDialog,QMessageBox
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from gui.PictureEditLabel import PictureEditLabel

class PictureEditWindow(QMainWindow):
    """
    Prozor koji predstavlja glavni editor slike

    Attributes:
        pictureToSend: slika koja se edituje
    """
    def __init__(self,object):
        """
        Konstruktor

        Args:
             object(Picture): slika koja se edituje u ovom prozoru
        """
        super(PictureEditWindow, self).__init__()
        self.pictureToSend = object
        self.updateWindow(self.pictureToSend)
        self.createMenuBar()

    def createMenuBar(self):
        """
        Kreira meni bar ovog prozora
        """
        bar = self.menuBar()
        filemenu = bar.addMenu("File")
        filemenu.addAction(QAction(QIcon("src/new.png"),"Load", self, triggered=self.loadA))
        filemenu.addAction(QAction(QIcon("src/delete.png"),"Close", self, triggered=self.closeA))

    def loadA(self):
        """
        Metoda koja nudi dijalog za ucitavanje nove slike i zatim je doda u edit prozor
        """
        image = QFileDialog.getOpenFileName(None, 'OpenFile', '', "Image file(*.png)")
        if image[0] != None:
            self.pictureToSend.setName(image[0].split("/")[-1])
            self.pictureToSend.setPicture(image[0])
            self.updateWindow(self.pictureToSend)

    def closeA(self):
        """
        Metoda koja zatvara otvorenu sliku u edit prozoru, i upozorava korisnika da ucita novu
        """
        tmpWidget = QWidget()
        self.setCentralWidget(tmpWidget)
        tmpMsg = QMessageBox()
        tmpMsg.setText("Currently opened picture closed, please choose a new one!")
        tmpMsg.setWindowIcon(QIcon("src/notification.png"))
        tmpMsg.setModal(True)
        tmpMsg.exec_()

    def updateWindow(self,picture):
        """
        Refresh edit prozora na prosledjenu sliku

        Args:
            picture(Picture): slika na koja se postavlja u edit prozor
        """
        self.mainEditor = PictureEditLabel(picture)
        tmpLayout = QVBoxLayout()
        tmpWidget = QWidget()
        tmpLayout.addWidget(self.mainEditor, Qt.FramelessWindowHint)
        self.mainEditor.show()
        self.mainEditor.setPosition(picture.getPosition())
        tmpWidget.setLayout(tmpLayout)
        self.setCentralWidget(tmpWidget)