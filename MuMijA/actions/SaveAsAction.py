from PySide2.QtWidgets import QAction, QApplication,QMessageBox
import os
import pickle
from actions.file_handler import FileHandler
from PySide2.QtWidgets import QInputDialog, QFileDialog
from PySide2.QtGui import QIcon

from shutil import copy
from model.Picture import Picture

BASE_DIR = os.path.join((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data")

RESERVED_TEMPORARY_NAME = "ReservedTemporaryName"


class SaveAsAction(QAction):
    """
    Klasa sadrzi metodu za cuvanje knjige uz promenu njenog imena u fizicku memoriju
    """

    def __init__(self):
        """
        Konstruktor
        """
        super(SaveAsAction, self).__init__("Save As")
        self.setIcon(QIcon("src/savingas.png"))
        self.triggered.connect(self.actionCalled)

    def actionCalled(self):
        """
        Prikazuje dijalog za unos imena po kome ce knjiga biti sacuvana, zatim prikazuje dijalog za biranje foldera i cuva instancu knjige u selektovan folder
        """
        bookName = QInputDialog.getText(None, "Name", "Enter desired name")
        bookName = bookName[0]
        if bookName != "":
            fh = FileHandler()
            currentOpenBook = QApplication.instance().tabWidget.currentWidget().model().getRoot()
            path = QFileDialog.getExistingDirectory(None, 'Path', 'Choose location to save the book')
            currentOpenBook.setPath(path)
            if os.path.isdir(os.path.join(path, bookName)):
                fh.createDirectory(BASE_DIR, RESERVED_TEMPORARY_NAME)
                for chapter in currentOpenBook.getChildren():
                    for page in chapter.getChildren():
                        for slot in page.getChildren():
                            if isinstance(slot, Picture):
                                copy(slot.getPicture(), os.path.join(BASE_DIR, RESERVED_TEMPORARY_NAME))
                                slot.setPicture(os.path.join(path, bookName, slot.getName()))
                fh.removeDirectory(path, bookName)
                fh.createDirectory(path, bookName)
                list = os.listdir(os.path.join(BASE_DIR, RESERVED_TEMPORARY_NAME))
                for i in list:
                    copy(os.path.join(BASE_DIR, RESERVED_TEMPORARY_NAME, i), os.path.join(path, bookName))
                fh.removeDirectory(BASE_DIR, RESERVED_TEMPORARY_NAME)
                data_path = os.path.join(path, bookName, bookName + ".pkl")
                with open(data_path, 'wb') as output:
                    currentOpenBook.setName(bookName)
                    pickle.dump(currentOpenBook, output, pickle.HIGHEST_PROTOCOL)
            if not os.path.isdir(os.path.join(path, bookName)) and not os.path.isfile(os.path.join(path, bookName)):
                fh.createDirectory(path, bookName)
                for chapter in currentOpenBook.getChildren():
                    for page in chapter.getChildren():
                        for slot in page.getChildren():
                            if isinstance(slot, Picture):
                                copy(slot.getPicture(), os.path.join(path, bookName))
                                slot.setPicture(os.path.join(path, bookName, slot.getName()))
                data_path = os.path.join(path, bookName, bookName + ".pkl")
                with open(data_path, 'wb') as output:
                    currentOpenBook.setName(bookName)
                    pickle.dump(currentOpenBook, output, pickle.HIGHEST_PROTOCOL)
            currentOpenBook.setPath(path)
            QApplication.instance().tabWidget.setTabText(QApplication.instance().tabWidget.currentIndex(), bookName)
        else:
            dialog = QMessageBox()
            dialog.setWindowTitle("Error")
            dialog.setText("Can't save a book without a name!")
            dialog.setWindowIcon(QIcon("src/notification.png"))
            dialog.setModal(True)
            dialog.exec_()