from PySide2.QtWidgets import QAction, QApplication,QMessageBox,QInputDialog
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget,QMainWindow, QLabel, QApplication, QFileDialog
from model.Workspace import Workspace
from model.Chapter import Chapter
from model.Book import Book
from model.Page import Page
from model.Text import Text
from model.Picture import Picture
from PySide2.QtGui import QIcon

class AddChildAction(QAction):
    """
    Klasa sadrzi akciju dodavanja child node na selektovanog roditelja u tree viewu
    """

    def __init__(self, parent):
        """
        Konstruktor

        Args:
            parent(Node): node na kom ce se prikazati akcija
        """
        super(AddChildAction, self).__init__("Add", parent)
        self.setIcon(QIcon("src/addnode.png"))
        self.triggered.connect(self.actionCalled)

    def actionCalled(self):
        """
        Dodaje child node
        """
        parent = QApplication.instance().selectionModel
        if isinstance(parent, Book):
            newName, ok = QInputDialog.getText(None, "New Chapter name", "Enter desired new name")
            if ok:
                if parent.isValidName(newName):
                    parent.addChild(Chapter(newName))

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
                                parent.addChild(Chapter(newName))
                                break
        if isinstance(parent, Chapter):
            if len(parent.getChildren())>0 :
                parent.addChild(Page(parent.getChildren()[-1].getName()[:-1]+str(int(parent.getChildren()[-1].getName()[-1:])+1)))
            else:
                parent.addChild(Page("Strana1"))
        if isinstance(parent, Page):
            item, ok = QInputDialog.getItem(QInputDialog(), "Add an element", "Choose one option:",
                                            ["Add text", "Add picture"], 0, False)
            if ok:
                if item == "Add text":
                    tmpList = []
                    for child in parent.getChildren():
                        if isinstance(child, Text):
                            tmpList.append(child)
                    if len(tmpList) > 0:
                        parent.addChild(Text(tmpList[-1].getName()[:-1] + str(int(tmpList[-1].getName()[-1:]) + 1)))
                    else:
                        parent.addChild(Text("Text1"))
                if item == "Add picture":
                    image = QFileDialog.getOpenFileName(None, 'OpenFile', '')
                    if image[1]:
                        path = image[0]
                        if path != None:
                            tmpPic = Picture(path.split("/")[-1])
                            tmpPic.setPicture(path)
                            parent.addChild(tmpPic)
