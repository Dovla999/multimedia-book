from PySide2.QtCore import Qt, QModelIndex
from PySide2.QtWidgets import QTreeView, QAbstractItemView, QMenu, QApplication
from model.Page import Page
from model.Chapter import Chapter
from gui.MyPictureEdit import MyPictureEdit
from gui.MyTextEdit import MyTextEdit
from model.Text import Text
from model.Picture import Picture


class HierarchyTreeView(QTreeView):
    """
    Graficki prikaz hijerarhijskog stabla uz implementiran kontekstni meni, i displayer za sadrzaj stranice

    """
    def __init__(self, model):
        """
        Konstruktor

        Uključuje opciju prikazivanja kontekstnog menija.

        """
        super(HierarchyTreeView, self).__init__()

        self.tree = model
        self.setModel(self.tree)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tree.removedPage.connect(self.Clear)
        self.tree.clearedSignal.connect(self.Clear)
        # ukljucuje kontekstni meni
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openMenu)

        selModel = self.selectionModel()
        selModel.selectionChanged.connect(self.updateTxt)
        selModel.selectionChanged.connect(self.updateSelection)
        self.lastSelectedPage=Page("tmp")
        self.lastSelectedIndex=QModelIndex()

    def getModel(self):
        """
        Vraca tree

        Return:
            Tree
        """
        return self.tree

    def openMenu(self, position):
        """
        Metoda povezana na customContextMenuRequested. Kreira kontekstni meni sa akcijama dodavanja, brisanja i promene naziva elemenata.
        Kontekstni meni se prikazuje na poziciji na kojoj se nalazio kursor misa.

        Args:
            position(QPoint): pozicija kursora misa

        """
        self.contextMenu = QMenu()

        actionManager = QApplication.instance().actionManager

        tmp = QApplication.instance().selectionModel
        if not isinstance(tmp, Text) and not isinstance(tmp, Picture):
            self.contextMenu.addAction(actionManager.addChildAction)
            self.contextMenu.addAction(actionManager.addAtAction)
            self.contextMenu.addAction(actionManager.addBefore)
            self.contextMenu.addSeparator()
            if not isinstance(tmp, Page):
                self.contextMenu.addAction(actionManager.renameNodeAction)
        #if isinstance(tmp, Picture):
            #self.contextMenu.addAction(actionManager.renameNodeAction)
        self.contextMenu.addAction(actionManager.removeChildAction)

        # prikaz kontekstnog menija
        self.contextMenu.exec_(self.viewport().mapToGlobal(position))

    def mousePressEvent(self, event):
        """
        Redefinisanje mouse pressed event-a.
        Uradjeno jer default-na implementacija rukovanja ovim dogadjajem ne podrazumeva deselekciju elementa stabla prilikom klika na praznu povrsinu.
        """

        if (self.selectionMode() == QAbstractItemView.SingleSelection):
            self.selectionModel().clear()
            self.clearSelection()
            self.setCurrentIndex(QModelIndex())

        super(HierarchyTreeView, self).mousePressEvent(event)

    def updateSelection(self, new):
        """
        Promena selekcije
        """
        if new.empty():
            self.SelectRoot()
        else:
            QApplication.instance().selectionModel = self.selectionModel().currentIndex().internalPointer()

    def Clear(self):
        """
        Refresh stranice
        """
        try:
            self.clearSelection()
            self.setCurrentIndex(self.lastSelectedIndex)
        except:
            pass

    def SelectRoot(self):
        """
        Selektovanje koren node
        """
        QApplication.instance().selectionModel = self.model().root

    def updateTxt(self):
        """
        Updateovanje status bara, labela za prikaz stranice, sadrzaja text i slika komponenti pri promeni selektovane strane
        """
        try:
            tmp=self.selectionModel().currentIndex().internalPointer()
            if isinstance(tmp, Page):
                self.lastSelectedIndex = self.selectionModel().currentIndex()
                widgetList = []
                j = 0
                for i in reversed(range(QApplication.instance().page.count())):
                    QApplication.instance().page.takeAt(i).widget().setParent(None)
                for child in tmp.getChildren():
                    try:
                        if isinstance(child, Text):
                            widget = MyTextEdit(child)
                            QApplication.instance().page.addWidget(widget, Qt.FramelessWindowHint)
                            widget.show()
                        if isinstance(child, Picture):
                            widget = MyPictureEdit(child)
                            QApplication.instance().page.addWidget(widget)
                            widget.show()
                        widgetList.append(widget)

                        for widget in widgetList:
                            widget.setPosition(widget.object.getPosition())
                    except Exception as e:
                        print(e)
                pageLabel = QApplication.instance().pageLabel
                pageLabel.setText(str(tmp.getName()[:-1]) + ": " + tmp.getName()[-1])
                self.lastSelectedPage = tmp
            if isinstance(tmp,Page):
                QApplication.instance().statusBar.setText(str(tmp.getParent().getParent().getName())+"->"+str(tmp.getParent().getName())+"->"+str(tmp.getName()))
            if isinstance(tmp,Chapter):
                QApplication.instance().statusBar.setText(str(tmp.getParent().getName())+"->"+str(tmp.getName()))
        except:
            pass


    def leftButtonPressed(self):
        """
        Prelazak na prethodnu stranu
        """
        try:
            tmp = self.lastSelectedIndex.sibling(self.lastSelectedPage.getIndex() - 1, 0)
            if tmp.isValid():
                self.setCurrentIndex(tmp)
                self.lastSelectedIndex = tmp
                self.lastSelectedPage = self.selectionModel().currentIndex().internalPointer()
            else:
                parent = self.lastSelectedIndex.parent()
                pageUncle = self.lastSelectedPage.getParent()
                book = pageUncle.getParent()
                index = pageUncle.getIndex()
                i = -1
                while len(book.childAt(index + i).getChildren()) == 0:
                    i -= 1
                parent = parent.sibling(self.lastSelectedPage.getParent().getIndex() + i, 0)
                i = 0
                isValid = True
                while isValid:
                    if parent.child(i, 0).isValid():
                        i += 1
                    else:
                        isValid = False
                parent = parent.child(i - 1, 0)
                if parent.isValid():
                    self.setCurrentIndex(parent)
                    self.lastSelectedIndex = parent
                    self.lastSelectedPage = self.selectionModel().currentIndex().internalPointer()
        except:
            pass

    def rightButtonPressed(self):
        """
        Prelazak na narednu stranu
        """
        try:
            tmp = self.lastSelectedIndex.sibling(self.lastSelectedPage.getIndex() + 1, 0)
            if tmp.isValid():
                self.setCurrentIndex(tmp)
                self.lastSelectedIndex = tmp
                self.lastSelectedPage = self.selectionModel().currentIndex().internalPointer()
            else:
                parent = self.lastSelectedIndex.parent()
                pageUncle = self.lastSelectedPage.getParent()
                book = pageUncle.getParent()
                index = pageUncle.getIndex()
                i = 1
                while len(book.childAt(index + i).getChildren()) == 0:
                    i += 1
                parent = parent.sibling(self.lastSelectedPage.getParent().getIndex() + i, 0)
                parent = parent.child(0, 0)
                if parent.isValid():
                    self.setCurrentIndex(parent)
                    self.lastSelectedIndex = parent
                    self.lastSelectedPage = self.selectionModel().currentIndex().internalPointer()
        except:
            pass