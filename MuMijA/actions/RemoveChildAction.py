from PySide2.QtWidgets import QAction, QApplication
from PySide2.QtGui import QIcon


class RemoveChildAction(QAction):
    """
    Klasa sadrzi metoda za logicko brisanje node-a
    """

    def __init__(self, parent):
        """
        Konstruktor

        Args:
            parent(Node): node na kom ce se prikazati akcija
        """
        super(RemoveChildAction, self).__init__("Remove", parent)
        self.setIcon(QIcon("src/removenode.png"))
        self.triggered.connect(self.remove)

    def remove(self):
        """
        Logicki brise trenutno selektovan node
        """
        child = QApplication.instance().selectionModel
        child.getParent().removeChild(child.getIndex())
