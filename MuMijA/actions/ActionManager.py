from actions.AddChildAction import AddChildAction
from actions.RemoveChildAction import RemoveChildAction
from actions.RenameNodeAction import RenameNodeAction
from actions.AddChildAtAction import AddChildAtAction
from actions.NewBookAction import NewBookAction
from actions.SaveAction import SaveAction
from actions.ImportBookAction import ImportBookAction
from actions.SaveAsAction import SaveAsAction
from actions.AddChildBefore import AddChildBeforeAction
from actions.DeleteAction import DeleteAction
from actions.RenameAction import RenameAction

class ActionManager(object):
    """
    Action manager, koristi se za pozivanje akcija poput add,remove, rename...
    """

    def __init__(self):
        """
        Konstruktor
        """
        self.addChildAction = AddChildAction(None)
        self.removeChildAction = RemoveChildAction(None)
        self.renameNodeAction = RenameNodeAction(None)
        self.addAtAction = AddChildAtAction(None)
        self.newBookAction = NewBookAction()
        self.saveAction = SaveAction()
        self.importBookAction = ImportBookAction()
        self.saveAsAction = SaveAsAction()
        self.addBefore = AddChildBeforeAction(None)
        self.deleteAction = DeleteAction()
        self.renameAction = RenameAction()
