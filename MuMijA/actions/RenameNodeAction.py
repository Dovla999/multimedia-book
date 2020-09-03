from PySide2.QtWidgets import QAction, QApplication
from model.Page import Page
from model.Chapter import Chapter
from model.Book import Book
from PySide2.QtWidgets import QMessageBox,QInputDialog
from PySide2.QtGui import QIcon
from model.Picture import Picture
import sys

class RenameNodeAction(QAction):
    """
    Klasa sadrzi metodu za menjanje imena node-a
    """

    def __init__(self, parent):
        """
        Konstruktor

        Args:
            parent(Node): node na kom ce se prikazati akcija
        """
        super(RenameNodeAction, self).__init__("Rename", parent)
        self.setIcon(QIcon("src/renamenode.png"))
        self.triggered.connect(self.rename)

    def rename(self):
        """
         Prikazuje dijalog za unos novog imena node-a, menja ime node-a
        """
        node = QApplication.instance().selectionModel
        parent = node.getParent()

        if isinstance(node, Chapter):
            newName, ok = QInputDialog.getText(None, "New Chapter name", "Enter desired new name")
            OK = False
            if ok:
                if parent.isValidName(newName):
                    OK = True
                else:
                    while not parent.isValidName(newName):
                        dialog = QMessageBox()
                        dialog.setWindowTitle("Error")
                        dialog.setText("That name is not valid")
                        dialog.setWindowIcon(QIcon("src/notification.png"))
                        dialog.setModal(True)
                        dialog.exec_()
                        newName, OK = QInputDialog.getText(None, "New Chapter name", "Enter desired new name")
                        if not OK:
                            break
                        else:
                            if parent.isValidName(newName):
                                break
            if ok and OK:
                node.setName(newName)
        if isinstance(node,Picture):
            newName, ok = QInputDialog.getText(None, "New Picture name", "Enter desired new name")
            if ok:
                node.setName(newName)
