from model.Node import Node
from PySide2.QtGui import QIcon
from PySide2.QtCore import QObject, Signal

class Book(Node):
    """
    Klasa naslednica klase Node, predstavlja knjigu

    Attributes:
        path: putanja knjige
    """
    def __init__(self, name):
        """
        Konstruktor

        Args:
            name(string): ime Book-a
        """
        super(Book, self).__init__(name)
        self.path = None

    def setPath(self, path):
        """
        Metoda koja postavlja putanju knjizi

        Args:
            path(String): putanja knjige
        """
        self.path = path

    def getPath(self):
        """
        Metoda koja vraca putanju knjige

        Return:
            Putanja knjige
        """
        return self.path

    def runRename(self):
        """
        Renamuje stranice da bi se odrzao redosled imena(Strana1,Strana2,...)
        """
        i = 1
        for chapter in self.getChildren():
            for page in chapter.getChildren():
                page.setName("Strana" + str(i))
                i += 1

    def __getstate__(self):
        """
        Metoda zaduzena za serijalizaciju
        """
        return {'name': self.name, 'parent': self.parent, 'children': self.children, 'path': self.path}

    def __setstate__(self, state):
        """
        Metoda zaduzena za deserijalizaciju

        Args:
            state: recnik koji sadrzi vrednosti atributa
        """
        super(Book, self).__init__("")
        self.name = state['name']
        self.parent = state['parent']
        self.children = state['children']
        self.path = state['path']
