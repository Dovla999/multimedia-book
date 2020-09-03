from PySide2.QtWidgets import QTextEdit,QApplication
from gui.TextEditDialog import TextEditDialog

class MyTextEdit(QTextEdit):
    """
    Text box koji se dodaje kao komponenta strane

    Attributes:
        object: tekst koji se dodaje u text box
    """
    def __init__(self, object):
        """
        Konstruktor

        Args:
             object(Text): tekst koji se postavlja na text box
        """
        super(MyTextEdit,self).__init__()
        self.object = object
        self.setText(object.getText())
        self.textChanged.connect(self.setObjectText)
        self.setStyleSheet("background-color:white;")
        self.setFixedHeight(150)
        self.setFixedWidth(300)
        self.setReadOnly(True)

    def mousePressEvent(self, event):
        """
        Rewrite mousePressEvent-a tako da se text box moze pomerati
        """
        self.windowPos = self.pos()
        self.mousePos = event.globalPos()
        super(QTextEdit, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """
        Rewrite mouseMoveEvent-a tako da se text box moze pomerati, i postavljanje poziciju text-a u slucaju da se text box pomeri
        """
        self.move(self.windowPos + event.globalPos() - self.mousePos)
        self.object.setPosition(self.geometry().topLeft())
        super(QTextEdit, self).mouseMoveEvent(event)

    def setPosition(self, position):
        """
        Postavlja text box na poziciju text-a u main window-u
        """
        if position is not None:
            self.move(position)
            super(QTextEdit, self).move(position)
            self.object.setPosition(self.geometry().topLeft())

    def mouseDoubleClickEvent(self, event):
        """
        Rewrite mouseDoubleClickEvent-a, otvara dijalog za editovanje text-a i update-uje status bar na trenutno stanje programa
        """
        QApplication.instance().statusBar.setText("Currently editing: " + str(
            self.object.getParent().getParent().getParent().getName() + "->" + self.object.getParent().getParent().getName()) + "->" + str(
            self.object.getParent().getName()) + "->" + self.object.getName())
        dialog = TextEditDialog(self.object)
        dialog.setModal(True)
        dialog.exec_()
        QApplication.instance().statusBar.setText(str(
            self.object.getParent().getParent().getParent().getName() + "->" + self.object.getParent().getParent().getName()) + "->" + str(
            self.object.getParent().getName()))

    def setObjectText(self):
        """
        Postavlja text-u kontekst text box-a
        """
        self.object.setText(self.toHtml())
