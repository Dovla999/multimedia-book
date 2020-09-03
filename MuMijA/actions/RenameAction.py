from PySide2.QtWidgets import QAction, QApplication
import os
import pickle
from actions.file_handler import FileHandler
from PySide2.QtWidgets import QInputDialog, QFileDialog, QMessageBox
from PySide2.QtGui import QIcon

from shutil import copy
from model.Picture import Picture

BASE_DIR = os.path.join((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data")

RESERVED_TEMPORARY_NAME = "ReservedTemporaryName"


class RenameAction(QAction):
    """
    Klasa sadrzi metodu za preimenovanje knjige
    """

    def __init__(self):
        """
        Konstruktor
        """
        super(RenameAction, self).__init__("Rename")
        self.setIcon(QIcon("src/rename.png"))
        self.triggered.connect(self.actionCalled)

    def actionCalled(self):
        """
        Prikazuje dijalog za unos novog imena knjige, preimenuje trenutno otvorenu knjigu u uneto ime
        """
        fh = FileHandler()
        currentOpenBook = QApplication.instance().tabWidget.currentWidget().model().getRoot()
        parent = QApplication.instance().model
        OK = False
        newName, ok = QInputDialog.getText(None, "New Book name", "Enter desired new name")
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
                    newName, OK = QInputDialog.getText(None, "New Book name", "Enter desired new name")
                    if not OK:
                        break
                    else:
                        if parent.isValidName(newName):
                            break
        bookName = newName
        path = currentOpenBook.getPath()
        if OK and ok:
            if path != None:
                if os.path.isdir(os.path.join(path, currentOpenBook.getName())):
                    fh.createDirectory(BASE_DIR, RESERVED_TEMPORARY_NAME)
                    for chapter in currentOpenBook.getChildren():
                        for page in chapter.getChildren():
                            for slot in page.getChildren():
                                if isinstance(slot, Picture):
                                    copy(slot.getPicture(), os.path.join(BASE_DIR, RESERVED_TEMPORARY_NAME))
                                    slot.setPicture(os.path.join(path, bookName, slot.getName()))
                    fh.removeDirectory(path, currentOpenBook.getName())
                    fh.createDirectory(path, bookName)
                    list = os.listdir(os.path.join(BASE_DIR, RESERVED_TEMPORARY_NAME))
                    for i in list:
                        copy(os.path.join(BASE_DIR, RESERVED_TEMPORARY_NAME, i), os.path.join(path, bookName))
                    fh.removeDirectory(BASE_DIR, RESERVED_TEMPORARY_NAME)
                    data_path = os.path.join(path, bookName, bookName + ".pkl")
                    with open(data_path, 'wb') as output:
                        currentOpenBook.setName(bookName)
                        pickle.dump(currentOpenBook, output, pickle.HIGHEST_PROTOCOL)
                currentOpenBook.setPath(path)
                QApplication.instance().tabWidget.setTabText(QApplication.instance().tabWidget.currentIndex(), bookName)
            else:
                currentOpenBook.setName(bookName)
                QApplication.instance().tabWidget.setTabText(QApplication.instance().tabWidget.currentIndex(), bookName)
