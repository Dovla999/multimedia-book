from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QMainWindow, QLabel, QApplication, QDockWidget, QPushButton, QGridLayout, \
    QVBoxLayout, QTabWidget, QInputDialog
from PySide2.QtGui import QIcon
from gui.EditMenu import EditMenu
from gui.HelpMenu import HelpMenu
from gui.ViewMenu import ViewMenu
from gui.FileMenu import FileMenu
from gui.MyToolbar import MyToolbar
from view.tree.HierarchyTreeModel import HierarchyTreeModel
from view.tree.HierarchyTreeView import HierarchyTreeView
from model.Book import Book
from model.Chapter import Chapter
from model.Page import Page

class MainWindow(QMainWindow):
    """
    Gui komponenta MainWindow
    """

    def __init__(self):
        """
        Konstruktor
        """
        super(MainWindow, self).__init__()
        self.init_toolbar()
        self.init_menu_bar()
        self.init_tree_main_widget()
        self.setFixedHeight(800)
        self.setFixedWidth(1000)
        self.setWindowIcon(QIcon("src/MuMijA_mainmenu.png"))
        self.statusBarLabel = QLabel("StatusBar")
        self.statusBar().addWidget(self.statusBarLabel, 1)

    def init_tree_main_widget(self):
        """
        Inicijalizuje layout main window-a, layout strane, tree, tabove, dugmadi i labele
        """
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.closeMyTab)
        leftDock = QDockWidget()
        leftDock.setFixedWidth(250)
        leftDock.setWidget(self.tabs)
        leftDock.setAllowedAreas(Qt.LeftDockWidgetArea)
        leftDock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        layout=QGridLayout()
        self.page = QVBoxLayout()
        self.central = QWidget()
        self.central.setFixedSize(730, 700)
        self.central.setLayout(self.page)
        self.central.setStyleSheet("background-color:white")
        self.LeftButton = QPushButton()
        self.PageLabel=QLabel()
        self.PageLabel.setAlignment(Qt.AlignCenter)
        self.PageLabel.setText("Nema trenutno otvorene strane")
        self.RightButton = QPushButton()
        self.LeftButton.setFixedSize(30, 30)
        self.RightButton.setFixedSize(30, 30)
        self.LeftButton.setIcon(QIcon("src/lbutton.png"))
        self.RightButton.setIcon(QIcon("src/rbutton.png"))
        layout.addWidget(self.central,0,0,1,5)
        layout.addWidget(self.LeftButton, 1, 1, 2, 1)
        layout.addWidget(self.PageLabel,1,2,2,1)
        layout.addWidget(self.RightButton, 1, 3, 2, 1)
        tmpWidget=QWidget()
        tmpWidget.setLayout(layout)
        self.setCentralWidget(tmpWidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, leftDock)

    def init_toolbar(self):
        """
        Inicijalizuje toolbar
        """
        self.addToolBar(Qt.TopToolBarArea, MyToolbar(self))

    def init_menu_bar(self):
        """
        Inicijalizuje menu bar
        """
        self.menuBar().addMenu(FileMenu())
        self.menuBar().addMenu(EditMenu())
        self.menuBar().addMenu(ViewMenu())
        self.menuBar().addMenu(HelpMenu())

    def newTab(self, root):
        """
        Inicijalizuje novi tab

        Return:
             Objekat book
        """
        if len(root.getChildren()) == 0:
            newName, ok = QInputDialog.getText(None, "New Chapter name", "Enter desired first chapter name")
            if not ok or newName == "":
                while not ok or newName == "":
                    newName, ok = QInputDialog.getText(None, "New Chapter name", "Enter desired first chapter name")
            root.addChild(Chapter(newName))
        book = Book(root.getName())
        book.setPath(root.getPath())
        book.setParent(QApplication.instance().model)
        rootModel = HierarchyTreeModel(book)
        rootView = HierarchyTreeView(rootModel)
        for chapter in root.getChildren():
            tmpChapter = Chapter(chapter.getName())
            book.addChild(tmpChapter)
            for page in chapter.getChildren():
                tmpPage = Page(page.getName())
                tmpChapter.addChild(tmpPage)
                for element in page.getChildren():
                    element.setParent(tmpPage)
                    tmpPage.addChild(element)
        self.tabs.addTab(rootView, root.getName())
        self.LeftButton.clicked.connect(rootView.leftButtonPressed)
        self.RightButton.clicked.connect(rootView.rightButtonPressed)
        rootView.SelectRoot()
        return book

    def closeMyTab(self, index):
        """
        Omogucava zatvaranje tab-a
        """
        child = self.tabs.widget(index).model().getRoot()
        child.getParent().removeChild(child.getIndex())
        self.tabs.removeTab(index)
