from PySide2.QtWidgets import QApplication, QMenu


class ViewMenu(QMenu):
    """
    Gui komponenta Viewmenu-a
    """

    def __init__(self):
        """
        Konstruktor
        """
        super(ViewMenu, self).__init__("View", None)
        self.addAction("PH")
        self.addAction("PH")
        self.addAction("PH")
