from PySide2.QtWidgets import QAction, QApplication
from PySide2.QtWidgets import QFileDialog
from PySide2.QtGui import QIcon
import os
import pickle

BASE_DIR = os.path.join((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data")


class ImportBookAction(QAction):
    """
    Klasa sadrzi metodu importovanja selektovane knjige
    """
    def __init__(self):
        """
        Konstruktor
        """
        super(ImportBookAction, self).__init__("Import")
        self.setIcon(QIcon("src/import.png"))
        self.triggered.connect(self.actionCalled)

    def actionCalled(self):
        """
        Importuje selektovanu knjigu sa ekstenzijom '.pkl'
        """
        parent = QApplication.instance().model
        path = QFileDialog.getOpenFileName(None, 'Open Book', '')
        if path[1]:
            with open(path[0], 'rb') as input:
                book = pickle.load(input)
            loadedBook = QApplication.instance().mainWindow.newTab(book)
            parent.addChild(loadedBook)
