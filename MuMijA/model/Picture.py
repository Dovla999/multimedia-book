from model.Node import Node
from PySide2.QtCore import QObject, Signal
from PySide2.QtGui import QIcon

class Picture(Node):
    """
    Klasa naslednica klase Node, predstavlja slika komponentu strane

    Attributes:
        picture: putanja slike
        position: pozicija slike u odnosu na glavni prozor aplikacije
    """
    def __init__(self, name):
        """
        Konstruktor

        Args:
             name(String): ime Picture-a
        """
        super(Picture, self).__init__(name)
        self.picture = ""
        self.position = None

    def setPicture(self,picture):
        """
        Postavlja putanju slike

        Args:
             picture(String): putanja slike
        """
        self.picture = picture

    def getPicture(self):
        """
        Vraca putanju slike

        Return:
             Putanja slike
        """
        return self.picture

    def setPosition(self,position):
        """
        Postavlja apsolutnu poziciju slike

        Args:
             position(QPoint()): apsolutna pozicija slike
        """
        self.position = position

    def getPosition(self):
        """
        Vraca apsolutnu poziciju slike

        Return:
             Apsolutna pozicija slike
        """
        return self.position

    def getIcon(self):
        """
        Metoda koja postavlja ikonicu slici

        Return:
            QIcon(): ikonica slike
        """
        return QIcon("src/pictureElement.png")

    def __getstate__(self):
        """
        Metoda zaduzena za serijalizaciju
        """
        return {'name': self.name, 'parent': self.parent, 'children': self.children, 'position': self.position,
                'picture': self.picture}

    def __setstate__(self, state):
        """
        Metoda zaduzena za deserijalizaciju

        Args:
            state: recnik koji sadrzi vrednosti atributa
        """
        super(Picture, self).__init__("")
        self.name = state['name']
        self.parent = state['parent']
        self.children = state['children']
        self.position = state['position']
        self.picture = state['picture']
