from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

class TextEditWindow(QMainWindow):
    """
    Glavni prozor u kome se edituje text

    Attributes:
        mainEdit: deo glavnog prozora u kome se dodaje i menja text
        textToSend: text koji je prikazan u mainEdit delu glavnog prostora
    """
    def __init__(self,object):
        """
        Konstruktor

        Args:
             object: text koji se edituje
        """
        super(TextEditWindow, self).__init__()
        self.mainEdit = QTextEdit()
        self.setCentralWidget(self.mainEdit)
        self.createToolBar()
        self.createMenuBar()
        self.textToSend = object
        self.mainEdit.document().setHtml(self.textToSend.getText())
        self.mainEdit.textChanged.connect(self.setTextToSend)

    def createToolBar(self):
        """
        Kreira tool bar deo glavnog prozora
        """
        tmpToolbar = QToolBar(self)
        self.boldAction = QAction(QIcon("src/bold.png"),"" ,self , triggered=self.textBold, checkable=True)
        self.italicAction = QAction(QIcon("src/italic.png"),"", self , triggered=self.textItalic, checkable=True)
        self.underlineAction = QAction(QIcon("src/underline.png"),"", self, triggered=self.textUnderline, checkable=True)
        pix = QPixmap(16, 16)
        pix.fill(Qt.black)
        self.textColorAction = QAction(QIcon(pix), "TextColor...", self,triggered=self.textColor)
        ##### font i velicina odavde
        fontBox = QFontComboBox(tmpToolbar)
        tmpToolbar.addWidget(fontBox)
        fontBox.activated[str].connect(self.textFontBox)
        tmpToolbar.addSeparator()
        #### velicina
        sizeBox = QComboBox(tmpToolbar)
        tmpToolbar.addWidget(sizeBox)
        sizeBox.setEditable(True)
        allSizes = QFontDatabase()
        for size in allSizes.standardSizes():
            sizeBox.addItem(str(size))
        sizeBox.activated[str].connect(self.textSizeBox)
        #### build-up toolbara
        tmpToolbar.addSeparator()
        tmpToolbar.addAction(self.boldAction)
        tmpToolbar.addSeparator()
        tmpToolbar.addAction(self.italicAction)
        tmpToolbar.addSeparator()
        tmpToolbar.addAction(self.underlineAction)
        tmpToolbar.addSeparator()
        tmpToolbar.addAction(self.textColorAction)
        self.addToolBar(Qt.TopToolBarArea, tmpToolbar)

    def textBold(self):
        """
        Metoda za pretvaranje dela text-a u bold format
        """
        fmt = QTextCharFormat()
        fmt.setFontWeight((self.boldAction.isChecked() and QFont.Bold) or QFont.Normal)
        self.mergeFormatOnWordOrSelection(fmt)

    def textUnderline(self):
        """
        Metoda za pretvaranje dela tezt-a u underline format
        """
        fmt = QTextCharFormat()
        fmt.setFontUnderline(self.underlineAction.isChecked())
        self.mergeFormatOnWordOrSelection(fmt)

    def textItalic(self):
        """
        Metoda za pretvaranje dela text-a u italic format
        """
        fmt = QTextCharFormat()
        fmt.setFontItalic(self.italicAction.isChecked())
        self.mergeFormatOnWordOrSelection(fmt)

    def textColor(self): # <<<<-----------------------------------------------------dovde stao
        """
        Metoda koja nudi izbor boja sa palete boja, a zatim pretvara deo text-a u izabranu boju
        """
        colour = QColorDialog.getColor(self.mainEdit.textColor(), self)
        if not colour.isValid():
            return
        fmt = QTextCharFormat()
        fmt.setForeground(colour)
        self.mergeFormatOnWordOrSelection(fmt)
        self.colorChanged(colour)

    def colorChanged(self, colour):
        """
        Metoda koja pretvara ikonicu izbora boja u izabranu boju sa palete boja

        Args:
            colour: izabrana boja sa palete boja
        """
        pix = QPixmap(16, 16)
        pix.fill(colour)
        self.textColorAction.setIcon(QIcon(pix))

    def textFontBox(self,fontBox):
        """
        Metoda koja pretvara deo text-a u izabrani font

        Args:
             fontBox(String): izabrani font
        """
        fmt = QTextCharFormat()
        fmt.setFontFamily(fontBox)
        self.mergeFormatOnWordOrSelection(fmt)

    def textSizeBox(self, sizeBox):
        """
        Metoda koja pretvara deo text-a u izabranu velicinu text-a u slucaju da je ta vrednost veca od 0

        Args:
             sizeBox(String): izabrana velicina text-a
        """
        pointSize = float(sizeBox)
        if pointSize > 0:
            fmt = QTextCharFormat()
            fmt.setFontPointSize(pointSize)
            self.mergeFormatOnWordOrSelection(fmt)

    def createMenuBar(self):
        """
        Kreira menu bar deo glavnog prozora
        """
        bar = self.menuBar()
        editmenu = bar.addMenu("Edit")
        editmenu.addAction(QAction(QIcon("src/undo.png"), "Undo", self, triggered=self.mainEdit.undo, shortcut="Ctrl+z"))
        editmenu.addAction(QAction(QIcon("src/redo.png"), "Redo", self, triggered=self.mainEdit.redo, shortcut="Shift+Ctrl+z"))
        editmenu.addAction(QAction(QIcon("src/copy.png"), "Copy", self, triggered=self.mainEdit.copy, shortcut=QKeySequence.Copy))
        editmenu.addAction(QAction(QIcon("src/cut.png"), "Cut", self, triggered=self.mainEdit.cut, shortcut=QKeySequence.Cut))
        editmenu.addAction(QAction(QIcon("src/paste.png"), "Paste", self, triggered=self.mainEdit.paste,shortcut=QKeySequence.Paste))
        editmenu.addAction(QAction(QIcon("src/deletetext.png"), "Delete", self, triggered=self.mainEdit.cut,shortcut=QKeySequence.Delete))
        editmenu.addAction(QAction(QIcon("src/selectall.png"), "Select All", self, triggered=self.mainEdit.selectAll,shortcut=QKeySequence.SelectAll))

    def mergeFormatOnWordOrSelection(self, format):
        '''
        Metoda koja uzima selektovani deo text-a, odnosno rec ispod kursora ako nista nije selektovano, i pravi adekvatne promene nad njim

        Args:
            format: format text-a u odnosu na koji se prave adekvatne promene
        '''
        cursor = self.mainEdit.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)
        cursor.mergeCharFormat(format)
        self.mainEdit.mergeCurrentCharFormat(format)

    def setTextToSend(self):
        """
        Metoda koja postavlja text text box delu stranice ukoliko se nacini promena text-a
        """
        self.textToSend.setText(self.mainEdit.toHtml())
        QApplication.instance().tabWidget.currentWidget().Clear()
