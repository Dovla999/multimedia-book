from PySide2.QtWidgets import QApplication, QMenu


class HelpMenu(QMenu):
    """
    Gui komponenta HelpMenu-a
    """

    def __init__(self):
        """
        Konstruktor
        """
        super(HelpMenu, self).__init__("Help", None)
        self.addAction("PH")
        self.addAction("PH")
        self.addAction("PH")