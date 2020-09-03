from PySide2.QtWidgets import QLabel,QApplication
from PySide2.QtGui import QPixmap
from gui.PictureEditDialog import PictureEditDialog

class MyPictureEdit(QLabel):
    """
    Labela sa slikom koja se dodaje na stranu

    Attributes:
        object: slika koja se dodaje u labelu
    """
    def __init__(self, object):
        """
        Konstruktor

        Args:
             object(Picture): slika koja se postavlja na labelu
        """
        super(MyPictureEdit,self).__init__()
        self.object = object
        self.setFixedHeight(150)
        self.setFixedWidth(150)
        self.setPixmap(QPixmap(self.object.getPicture()).scaled(150, 150))

    def setPosition(self, position):
        """
        Postavlja labelu na poziciju slike u main window-u
        """
        if position is not None:
            self.move(position)
            super(QLabel, self).move(position)
            self.object.setPosition(self.geometry().topLeft())

    def mouseDoubleClickEvent(self, event):
        """
        Rewrite mouseDoubleClickEvent-a, otvara dijalog za editovanje slike i update-uje status bar na trenutno stanje programa
        """
        QApplication.instance().statusBar.setText("Currently editing: " + str(
            self.object.getParent().getParent().getParent().getName() + "->" + self.object.getParent().getParent().getName()) + "->" + str(
            self.object.getParent().getName()) + "->" + self.object.getName())
        dialog = PictureEditDialog(self.object)
        dialog.setModal(True)
        dialog.exec_()
        QApplication.instance().statusBar.setText(str(
            self.object.getParent().getParent().getParent().getName() + "->" + self.object.getParent().getParent().getName()) + "->" + str(
            self.object.getParent().getName()))
