from model.Node import Node
from PySide2.QtCore import QObject, Signal
from PySide2.QtGui import QIcon

class Text(Node):
    """
    Klasa naslednica klase Node, predstavlja text komponentu strane

    Attributes:
        text: tekstualni sadrzaj text-a
        position: pozicija text-a u odnosu na glavni prozor aplikacije
    """
    def __init__(self, name):
        """
        Konstruktor

        Args:
             name(String): ime Text-a
        """
        super(Text, self).__init__(name)
        self.text = ""
        self.position = None

    def setText(self,text):
        """
        Postavlja tekstualni sadrzaj text-u

        Args:
             text(String): tekstualni sadrzaj text-a
        """
        self.text = text

    def getText(self):
        """
        Vraca tekstualni sadrzaj text-a

        Return:
             Tekstualni sadrzaj text-a
        """
        return self.text

    def setPosition(self,position):
        """
        Postavlja apsolutnu poziciju text-a

        Args:
             position(QPoint()): apsolutna pozicija text-a
        """
        self.position = position

    def getPosition(self):
        """
        Vraca apsolutnu poziciju text-a

        Return:
             Apsolutna pozicija text-a
        """
        return self.position

    def getIcon(self):
        """
        Metoda koja postavlja ikonicu text-u

        Return:
            QIcon(): ikonica text-a
        """
        return QIcon("src/textElement.png")

    def __getstate__(self):
        """
        Metoda zaduzena za serijalizaciju
        """
        return {'name': self.name, 'parent': self.parent, 'children': self.children, 'position': self.position,
                'text': self.text}

    def __setstate__(self, state):
        """
        Metoda zaduzena za deserijalizaciju

        Args:
            state: recnik koji sadrzi vrednosti atributa
        """
        super(Text, self).__init__("")
        self.name = state['name']
        self.parent = state['parent']
        self.children = state['children']
        self.position = state['position']
        self.text = state['text']
