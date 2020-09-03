from model.Node import Node
from PySide2.QtGui import QIcon
from PySide2.QtCore import QObject, Signal

class Page(Node):
    """
    Klasa naslednica klase Node, predstavlja stranu

    Attributes:
        text: text koji stranica sadrzi
    """
    def __init__(self, name):
        """
        Konstruktor

        Args:
            name(string): ime Page-a
        """
        super(Page, self).__init__(name)

    def getIcon(self):
        """
        Metoda koja postavlja ikonicu stranici

        Return:
            QIcon(): ikonica stranice
        """
        return QIcon("src/page.png")

    def __getstate__(self):
        """
        Metoda zaduzena za serijalizaciju
        """
        return {'name': self.name, 'parent': self.parent, 'children': self.children}

    def __setstate__(self, state):
        """
        Metoda zaduzena za deserijalizaciju

        Args:
            state: recnik koji sadrzi vrednosti atributa
        """
        super(Page, self).__init__("")
        self.name = state['name']
        self.parent = state['parent']
        self.children = state['children']
