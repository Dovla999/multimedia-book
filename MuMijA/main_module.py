import sys

from PySide2.QtWidgets import QApplication, QInputDialog
from PySide2.QtGui import QIcon
from actions.ActionManager import ActionManager
from gui.MainWindow import MainWindow
from model.Workspace import Workspace
from model.Book import Book
import atexit

import os
import pickle
from actions.file_handler import FileHandler

from shutil import copy
from model.Picture import Picture

BASE_DIR = os.path.join((os.path.dirname(os.path.abspath(__file__))), "data")

RESERVED_TEMPORARY_NAME = "ReservedTemporaryName"

def exit_handler():
    item, ok = QInputDialog.getItem(QInputDialog(), "Save workspace", "Choose one option:",
                                    ["Save current state", "Discard current state"], 0, False)
    if ok and item == "Save current state":
        with open("lastActiveWorkspace.txt", "w") as file:
            for child in QApplication.instance().model.getChildren():
                fh = FileHandler()
                currentOpenBook = child
                bookName = currentOpenBook.getName()
                if currentOpenBook.getPath() == None:
                    path = BASE_DIR
                else:
                    path = currentOpenBook.getPath()
                currentOpenBook.setPath(path)
                file.write(
                    currentOpenBook.getPath() + "\\" + currentOpenBook.getName() + "\\" + currentOpenBook.getName() + ".pkl" + "\n")
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
                        pickle.dump(currentOpenBook, output, pickle.HIGHEST_PROTOCOL)
    else:
        with open("lastActiveWorkspace.txt", "w") as file:
            file.write("")

if __name__ == '__main__':
    atexit.register(exit_handler)
    app = QApplication(sys.argv)
    rootNode = Workspace("Workspace")
    app.model = rootNode
    app.selectionModel = rootNode
    app.actionManager = ActionManager()
    mainWindow = MainWindow()
    mainWindow.setWindowTitle("MuMijA")
    app.page = mainWindow.page
    app.mainWidget = mainWindow.central
    app.statusBar = mainWindow.statusBarLabel
    app.pageLabel = mainWindow.PageLabel
    app.tabWidget = mainWindow.tabs
    app.mainWindow=mainWindow
    mainWindow.show()
    item, ok = QInputDialog.getItem(QInputDialog(), "Restoration", "Restore last saved workspace, choose one option:",
                                    ["Restore", "Create new"], 0, False)
    if ok:
        if item == "Restore":
            with open("lastActiveWorkspace.txt", "r") as file:
                for line in file:
                    with open(line.replace("\n", ""), 'rb') as input:
                        book = pickle.load(input)
                    loadedBook = QApplication.instance().mainWindow.newTab(book)
                    rootNode.addChild(loadedBook)
    sys.exit(app.exec_())
