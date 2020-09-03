from model.Node import Node
from PySide2.QtCore import QObject, Signal

class Workspace(Node):
    """
    Klasa naslednica klase Node, predstavlja workspace
    """
    def __init__(self, name):
        """
        Konstruktor

        Args:
            name: ime workspace-a
        """
        super(Workspace, self).__init__(name)
        self.setParent(None)

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
        super(Workspace, self).__init__("")
        self.name = state['name']
        self.parent = state['parent']
        self.children = state['children']
