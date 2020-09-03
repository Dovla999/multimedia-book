from PySide2.QtCore import QObject, Signal
from PySide2.QtGui import QIcon

class Node(QObject):
    """
    Node u stablu, može se koristiti kao root klasa za dokument, projekat, paket...

    Args:
      name (str): Naziv čvora.

    Attributes:
      name (str): naziv node-a
      parent (Node): node na visem nivou hijerarhije
      children (list(Node)): lista node-ova na nizem nivou hijerarhije
      path(str): apsolutna putanja node-a
    """
    '''
        Signal prilikom dodavanja child node-a

        Args:
            parent(object): node  u koji se dodaje
            position(int): pozicija na koju se dodaje
    '''
    childInsertStartSignal = Signal(object, int)
    '''
        Signal prilikom dodavanja child node-a

        Args:
            parentNode(object): node u koji se dodaje
            addedNode(object): node koji se dodaje
    '''
    childInsertedSignal = Signal(object, object)
    '''
        Signal prilikom dodavanja child node-a

        Args:
            parent(object): node iz kojeg se brise
            position(int): pozicija sa koje se brise
    '''
    childRemoveStartSignal = Signal(object, int)
    '''
        Signal prilikom uklanjanja child node-a

        Args:
            parentNode(object): node iz kojeg se uklanja
            childNode(object): node koji se uklanja
            position(int): pozicija sa koje se uklanja
    '''
    childRemovedSignal = Signal(object, object, int)


    def __init__(self, name):
        """
        Konstruktor

        Args:
            name(int): naziv node-a
        """
        super(Node, self).__init__()
        self.name = name
        self.parent = None
        self.children = []


    def setParent(self, parent):
        """
        Postavlja roditeljski node

        Args:
            parent(Node): roditeljski node
        """
        self.parent = parent

    def getParent(self):
        """
        Vraca roditeljski node

        Return:
            Roditeljski node; None ukoliko je element na vrhu hijerarhije
        """
        return self.parent

    def setName(self, name):
        """
        Postavlja naziv node-a

        Args:
            name(string): naziv node-a
        """
        self.name = name

    def getName(self):
        """
        Vraca naziv node-a

        Return:
            Naziv node-a
        """
        return self.name

    def getChildren(self):
        """
        Vraca listu child node-ova

        Return:
             Lista children
        """
        return self.children

    def setChildren(self, children):
        """
        Postavlja listu children

        Args:
            children: lista children
        """
        self.children = children

    def childCount(self):
        """
        Vraca broj child node-ova

        Return:
             Broj elemenata liste children
        """
        return len(self.children)

    def addChild(self, child):
        """
        Dodaje child na kraj liste

        Args:
            child(Node): node koji se dodaje
        """
        self.childInsertStartSignal.emit(self, self.childCount())
        self.children.append(child)
        child.setName(child.getName())
        child.setParent(self)
        self.childInsertedSignal.emit(self, child)

    def insertChild(self, position, child):
        """
        Ubacuje child na odredjenu poziciju

        Args:
            position(int): pozicija u listi na koju se ubacuje
            child(Node): node koji se ubacuje

        Return:
            True ako je uspesno ubacivanje, False za neispravnu poziciju
        """
        if position < 0 or position > len(self.children):
            return False

        self.childInsertStartSignal.emit(self, position)
        self.children.insert(position, child)
        child.setParent(self)
        self.childInsertedSignal.emit(self, child)
        return True

    def removeChild(self, position):
        """
        Izbacuje child sa odredjene pozicije

        Args:
            position(int): pozicija u listi sa koje se izbacuje

        Return:
            True ako je uspesno izbacivanje, False za neispravnu poziciju
        """
        if position < 0 or position > len(self.children) - 1:
            return False
        child = self.childAt(position)

        self.childRemoveStartSignal.emit(self, position)

        self.children.pop(position)
        self.childRemovedSignal.emit(self, child, position)

        return True

    def childAt(self, row):
        """
        Vraca child node na zadatoj poziciji

        Args:
            row(int): pozicija node-a u listi

        Return:
            Node na zadatoj poziciji (Node); None za neispravnu poziciju
        """
        if row < 0 or row > len(self.children) - 1:
            return None
        else:
            return self.children[row]

    def getIndex(self):
        """
        Vraca poziciju elementa u listi child-ova roditeljskog elementa

        Return:
            pozicija u listi child-ova parent node-a
        """
        if (self.parent is not None):
            return self.parent.children.index(self)

    def getIcon(self):
        """
        Vraca ikonicu za prikaz u stablu

        Return:
            ikonica za prikaz (QIcon)
        """
        return QIcon("../folder.png")

    def isValidName(self, name):
        if name == "":
            return False
        for child in self.getChildren():
            if name == child.getName():
                return False
        return True

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
        super(Node, self).__init__("")
        self.name = state['name']
        self.parent = state['parent']
        self.children = state['children']
