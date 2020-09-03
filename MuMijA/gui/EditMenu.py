from PySide2.QtWidgets import QApplication, QMenu


class EditMenu(QMenu):
    """
    Gui komponenta EditMenu-a
    """

    def __init__(self):
        """
        Konstruktor
        """
        super(EditMenu, self).__init__("Edit", None)
        self.addAction("PH")
        self.addAction("PH")
        self.addAction("PH")
