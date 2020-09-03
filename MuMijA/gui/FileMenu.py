from PySide2.QtWidgets import QApplication, QMenu


class FileMenu(QMenu):
    """
    Gui komponenta FileMenu-a
    """

    def __init__(self):
        """
        Konstruktor
        """
        super(FileMenu, self).__init__("File", None)
        actionManager = QApplication.instance().actionManager
        self.addAction(actionManager.newBookAction)
        self.addSeparator()
        self.addAction(actionManager.saveAction)
        self.addSeparator()
        self.addAction(actionManager.importBookAction)
        self.addSeparator()
        self.addAction(actionManager.saveAsAction)
        self.addSeparator()
        self.addAction(actionManager.deleteAction)
        self.addSeparator()
        self.addAction(actionManager.renameAction)