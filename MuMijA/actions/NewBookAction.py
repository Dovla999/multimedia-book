from PySide2.QtWidgets import QAction, QApplication, QMessageBox, QInputDialog
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget, QMainWindow, QLabel, QApplication, QFileDialog
from model.Workspace import Workspace
from model.Chapter import Chapter
from model.Book import Book
from model.Page import Page
from model.Text import Text
from model.Picture import Picture
from PySide2.QtGui import QIcon


class NewBookAction(QAction):
    """
    Klasa sadrzi akciju dodavanja book node-a na workspace
    """

    def __init__(self):
        """
        Konstruktor
        """
        super(NewBookAction, self).__init__("New Book")
        self.setIcon(QIcon("src/new.png"))
        self.triggered.connect(self.actionCalled)

    def actionCalled(self):
        """
        Prikazuje dijalog za unos imena nove knjige, kreira novu instancu knjige sa unetim imenom
        """
        parent = QApplication.instance().model
        newName, ok = QInputDialog.getText(None, "New Book name", "Enter desired new name")
        if ok:
            if parent.isValidName(newName):
                newBook = Book(newName)
                book = QApplication.instance().mainWindow.newTab(newBook)
                parent.addChild(book)

            else:
                while not parent.isValidName(newName):
                    dialog = QMessageBox()
                    dialog.setWindowTitle("Error")
                    dialog.setText("That name is not valid")
                    dialog.setWindowIcon(QIcon("src/notification.png"))
                    dialog.setModal(True)
                    dialog.exec_()
                    newName, cancel = QInputDialog.getText(None, "New Book name", "Enter desired new name")
                    if not cancel:
                        break
                    else:
                        if parent.isValidName(newName):
                            newBook = Book(newName)
                            book = QApplication.instance().mainWindow.newTab(newBook)
                            parent.addChild(book)
                            break
