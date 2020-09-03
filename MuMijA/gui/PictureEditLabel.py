from PySide2.QtWidgets import QLabel,QApplication
from PySide2.QtGui import QPixmap

class PictureEditLabel(QLabel):
    """
    Labela sa slikom koja se edituje

    Attributes:
        object: slika koja se edituje
    """
    def __init__(self, object):
        """
        Konstruktor

        Args:
             object(Picture): slika koja se edituje
        """
        super(PictureEditLabel, self).__init__()
        self.object = object
        self.setFixedHeight(150)
        self.setFixedWidth(150)
        self.setPixmap(QPixmap(self.object.getPicture()).scaled(150, 150))

    def mousePressEvent(self, event):
        """
            Rewrite mousePressEvent-a tako da se labela moze pomerati
        """
        self.windowPos = self.pos()
        self.mousePos = event.globalPos()
        super(QLabel, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """
            Rewrite mouseMoveEvent-a tako da se labela moze pomerati, i postavljanje poziciju slike u slucaju da se labela pomeri
        """
        self.move(self.windowPos + event.globalPos() - self.mousePos)
        super(QLabel, self).mouseMoveEvent(event)
        self.object.setPosition(self.geometry().topLeft())
        QApplication.instance().tabWidget.currentWidget().Clear()

    def setPosition(self, position):
        """
            Postavlja labelu na poziciju slike u main window-u
        """
        if position is not None:
            self.move(position)
            super(QLabel, self).move(position)
            self.object.setPosition(self.geometry().topLeft())