from PySide2.QtWidgets import QApplication, QToolBar


class MyToolbar(QToolBar):
    """
    Gui komponenta Toolbar-a
    """

    def __init__(self, parent):
        """
        Konstruktor
        """
        super(MyToolbar, self).__init__(parent)
