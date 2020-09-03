from PySide2.QtWidgets import QAction, QApplication, QMessageBox, QInputDialog

from model.Workspace import Workspace
from model.Chapter import Chapter
from model.Book import Book
from model.Page import Page
from PySide2.QtGui import QIcon


class AddChildAtAction(QAction):
    """
    Klasa sadrzi akciju insertovanja child node na selektovanog siblinga u tree viewu
    """

    def __init__(self, parent):
        """
        Konstruktor

        Args:
             parent(Node): node na kom ce se prikazati akcija
        """
        super(AddChildAtAction, self).__init__("Add At", parent)
        self.setIcon(QIcon("src/addat.png"))
        self.triggered.connect(self.actionCalled)

    def actionCalled(self):
        """
        Dodaje sibling node, insertuje novi node izmedju selektovanog i njegovog narednog
        """
        sibling = QApplication.instance().selectionModel
        parent = sibling.getParent()

        if isinstance(sibling, Chapter):
            newName, ok = QInputDialog.getText(None, "New Chapter name", "Enter desired new name")
            if ok:
                if parent.isValidName(newName):
                    parent.insertChild(sibling.getIndex() + 1, Chapter(newName))

                else:
                    while not parent.isValidName(newName):
                        dialog = QMessageBox()
                        dialog.setWindowTitle("Error")
                        dialog.setText("That name is not valid")
                        dialog.setWindowIcon(QIcon("src/notification.png"))
                        dialog.setModal(True)
                        dialog.exec_()
                        newName, cancel = QInputDialog.getText(None, "New Chapter name", "Enter desired new name")
                        if not cancel:
                            break
                        else:
                            if parent.isValidName(newName):
                                parent.insertChild(sibling.getIndex() + 1, Chapter(newName))
                                break

        if isinstance(sibling, Page):
            if len(sibling.getParent().getChildren()) > 0:
                sibling.getParent().insertChild(sibling.getIndex() + 1,
                                                Page(sibling.getName()[:-1] + str(int(sibling.getName()[-1:]) + 1)))
            else:
                sibling.getParent().addChild(Page("Strana1"))
