from PySide2.QtWidgets import QAction, QApplication,QDialog,QMessageBox
from PySide2.QtGui import QIcon
from actions.file_handler import FileHandler
import os
import shutil
BASE_DIR = os.path.join((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data")

class DeleteAction(QAction):
    """
    Klasa sadrzi metodu za brisanje knjige iz memorije
    """

    def __init__(self):
        """
        Konstruktor
        """
        super(DeleteAction, self).__init__("Delete")
        self.setIcon(QIcon("src/delete.png"))
        self.triggered.connect(self.actionCalled)

    def actionCalled(self):
        """
        Brise knjigu sa fizicke memorije ako knjiga sa takvim imenom postoji, ako ne postoji onda upozori korisnika o tome
        """
        fh=FileHandler()
        currentOpenBook = QApplication.instance().tabWidget.currentWidget().model().getRoot()
        if currentOpenBook.getPath() != None:
            fh.removeDirectory(currentOpenBook.getPath(),currentOpenBook.getName())
            QApplication.instance().tabWidget.tabCloseRequested.emit(QApplication.instance().tabWidget.currentWidget())
        else:
            dialog = QMessageBox()
            dialog.setWindowTitle("Error")
            dialog.setText("Current book is not saved anywhere")
            dialog.setWindowIcon(QIcon("src/notification.png"))
            dialog.setModal(True)
            dialog.exec_()