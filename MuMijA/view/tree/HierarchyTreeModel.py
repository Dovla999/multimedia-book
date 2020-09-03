from PySide2.QtCore import QAbstractItemModel, QModelIndex, Qt, Signal
from model.Node import Node
from model.Chapter import Chapter
from model.Picture import Picture
from model.Text import Text
from model.Page import Page

class HierarchyTreeModel(QAbstractItemModel):
    """
    Model hijerarhijskog stabla

    Args:
      root (Node): korenski node

    Attributes:
      root (Node): korenski node

    """
    '''
    Signal prilikom brisanja page-a
    '''
    removedPage = Signal(object)
    clearedSignal = Signal(object)

    def __init__(self, root):
        """
        Konstruktor

        Args:
            root(Node): korenski node stabla
        """
        super(HierarchyTreeModel, self).__init__()
        self.root = root
        root.childInsertStartSignal.connect(self.beginAddChild)
        root.childInsertedSignal.connect(self.addChild)
        root.childRemoveStartSignal.connect(self.beginRemoveChild)
        root.childRemovedSignal.connect(self.removeChild)

    def getRoot(self):
        """
        Vraca korenski node

        Return:
            Korenski node
        """
        return self.root

    def rowCount(self, parent=QModelIndex()):
        """
        Vraca broj redova (podelemenata) elementa stabla

        Args:
            parent(QModelIndex): indeks elementa ciji se broj podelemenata trazi

        Return:
            Broj elemenata
        """
        if not parent.isValid():
            parentNode = self.root
        else:
            parentNode = parent.internalPointer()

        return parentNode.childCount()

    def columnCount(self, parent):
        """
        Vraca broj kolona elementa stabla

        Args:
            parent(QModelIndex): indeks elementa ciji se broj kolona trazi

        Return:
            Za model namenjen kreiranju stabla uvek vraca 1
        """
        return 1

    def data(self, index, role):
        """
        Vraca podatke iz modela za prikaz u viewer-u

        Args:
            index(QModelIndex): indeks elementa ciji se podaci traze
            role(QtCore.Qt.ItemDataRole): vrsta podataka koji se traze

        Return:
            Naziv cvora za DisplayRole, ikonica za DecorationRole, None za ostalo
        """
        if not index.isValid():
            return None

        node = index.internalPointer()

        if role == Qt.DisplayRole:
            return node.getName()

        if role == Qt.DecorationRole:
            return node.getIcon()

    def headerData(self, section, orientation, role):
        """
        Vraca podatke za zaglavlje viewer-a

        Args:
            section(int): redni broj reda/kolone zaglavlja
            orientation(QtCore.Qt.Orientation): da li je podatak namenjen prikazu u zaglavlju reda ili kolone
            role(QtCore.Qt.ItemDataRole): vrsta podataka koji se traze

        Return:
            Tekst "Document explorer" za DisplayRole, None za ostalo
        """
        if role == Qt.DisplayRole:
            return "Document explorer"

    def flags(self, index):
        """
        Podesava dozvoljene nacine pristupa elementu stabla

        Args:
            index(QModelIndex): indeks elementa cije se ponasanje definise

        Return:
            Dozvoljeni nacini pristupa (Qt.ItemFlag) povezani logickim operatorom "ILI"

        """
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def index(self, row, column, parent):
        """
        Kreira QModelIndex

        Args:
            row(int): broj reda elementa
            column(int): broj kolone elementa
            parent(QModelIndex): element u kojem se nalazi element za koji se indeks kreira

        Return:
            QModelIndex sa instancom klase Node kao vrednoscu internalPointer-a; Prazan (nevalidan) QModelIndex za nepostojeci child element na toj poziciji

        """
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentNode = self.root
        else:
            parentNode = parent.internalPointer()

        childItem = parentNode.childAt(row)
        if (childItem):
            return self.createIndex(row, 0, childItem)
        else:
            return QModelIndex()

    def parent(self, index):
        """
        Vraca indeks roditeljskog elementa

        Args:
            index(QModelIndex): indeks elementa ciji se parent trazi

        Return:
            QModelIndex sa parent Node-om kao vrednoscu internalPointer-a; prazan (nevalidan) QModelIndex ako je index==root

        """

        node = index.internalPointer()

        if not isinstance(node, Node):
            return QModelIndex()
        parentNode = node.getParent()

        if parentNode is None or parentNode == self.root:
            return QModelIndex()

        return self.createIndex(parentNode.getIndex(), 0, parentNode)

    def beginAddChild(self, parent, position):
        """
        Osvezavanje stabla nakon dodavanja

        Args:
            parent(Node): node u koji će biti dodat node
            position(int): pozicija na koju će biti dodat node

        """
        if parent == self.root:
            self.beginInsertRows(QModelIndex(), position, position)
        else:
            self.beginInsertRows(self.createIndex(parent.getIndex(), 0, parent), position, position)

    def addChild(self, parent, child):
        """
        Osvezavanje stabla nakon dodavanja

        Args:
            parent(Node): node u koji je izvrseno dodavanje
            child(Node): node koji je dodat

        """
        self.endInsertRows()
        child.childInsertedSignal.connect(self.addChild)
        child.childInsertStartSignal.connect(self.beginAddChild)
        child.childRemovedSignal.connect(self.removeChild)
        child.childRemoveStartSignal.connect(self.beginRemoveChild)
        if isinstance(child,Text) or isinstance(child,Picture):
            self.calledClear()
        if isinstance(parent, Chapter):
            parent.getParent().runRename()

    def beginRemoveChild(self, parentNode, position):
        """
        Priprema stabla za uklanjanje node-a

        Args:
            parent(Node): node iz kojeg se uklanja node
            position(int): pozicija sa koje se uklanja node

        """
        if parentNode == self.root:
            parent = QModelIndex()
        else:
            parent = self.createIndex(parentNode.getIndex(), 0, parentNode)

        self.beginRemoveRows(parent, position, position)

    def removeChild(self, parentNode, childNode, position):
        """
        Osvezavanje stabla nakon uklanjanja, ukoliko je uklonjena stranica takodje popravlja imena stranica u tom poglavlju, i emituje signal da je stranica obrisana

        Args:
            parentNode(Node): node iz kojeg je uklonjen node
            childNode(Node): node koji se uklanja
            position(int): pozicija sa koje je uklonjen node

        """
        self.endRemoveRows()
        if isinstance(parentNode, Chapter):
            parentNode.getParent().runRename()
            self.removedPage.emit(self)
        if isinstance(parentNode, Page):
            self.calledClear()

    def calledClear(self):
        """
        Emit-uje signal za clear TreeView-a
        """
        self.clearedSignal.emit(self)
