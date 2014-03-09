import sys
import math
import PyQt4
from PyQt4 import QtGui
from entrywidget import Ui_EntryWidget
import mainwindow
import core


def main():
    """Sets up ui from qt .ui file."""

    app = QtGui.QApplication(sys.argv)
    mw = QtGui.QMainWindow()
    ui = mainwindow.Ui_MainWindow()
    ui.setupUi(mw)
    master = MasterHandler()
    master.ui = ui
    mwHandler = MainWindowHandler(mw, ui)
    master.mainWindowHandler = mwHandler
    mwHandler.initMainWindow()

    dbh = initDB(master, ui)
    master.databaseHandler = dbh

    interface = MainInterfaceHandler(master)
    master.mainInterfaceHandler = interface

    mw.show()
    dbh.resized()

    testing(ui, dbh)

    sys.exit(app.exec_())
    return


def initDB(master, ui):
    db = core.Database()
    grid = ui.entryView.layout()

    # ui.entryView.setFixedHeight(400)

    dbh = DatabaseHandler(master, db)
    ui.centralwidget.resizeEvent = dbh.resizeEvent

    dbh.resized()
    return dbh

class MasterHandler(object):
    """Handles references to all major objects."""

    def __init__(self):
        self.ui = None
        self.mainWindowHandler = None
        self.mainInterfaceHandler = None
        self.databaseHandler = None


class MainInterfaceHandler(object):
    """Handler for the header interface and buttons."""

    def __init__(self, master):
        self.master = master
        self.ui = master.ui 
        self.sortKey = core.Database.SORT_BY_TIME_EDITED

        self.btnNewEntry = self.ui.btnNewEntry
        self.btnNewEntry.clicked.connect(self.addNewEntry)

        self.sortSelector = self.ui.sortSelector
        self.sortSelector.addItem("Time Created", core.Database.SORT_BY_TIME_CREATED)
        self.sortSelector.addItem("Time Edited", core.Database.SORT_BY_TIME_EDITED)

        self.sortSelector.currentIndexChanged.connect(self.sortingMethodChanged)

        self.btnSort = self.ui.btnSort
        self.btnSort.clicked.connect(self.sort)

    def sort(self):
        self.master.databaseHandler.reSort()

    def sortingMethodChanged(self):
        self.sortKey = self.sortSelector.itemData(self.sortSelector.currentIndex())


    def addNewEntry(self):
        self.master.databaseHandler.addEntry(core.Entry())
        self.master.databaseHandler.reSort()

class MainWindowHandler(object):
    """Main event handler for ui"""

    def __init__(self, mainWindow, ui):
        super(MainWindowHandler, self).__init__()

        self.mw = mainWindow
        self.ui = ui
        # self.btnEditEntry = ui.btnEditEntry

    def initMainWindow(self):
        """ Sets up main GUI window. """
        pass


class EntryHandler(object):
    """Handles all interactions with Entries and their Widgets."""

    def __init__(self, master, entry):
        self.master = master
        self.ui = master.ui
        self.entry = entry
        self.buildWidget()

        self.setText(entry.getText())
        return

    def buildWidget(self):
        self.widget = QtGui.QWidget()
        self.ui = Ui_EntryWidget()
        self.ui.setupUi(self.widget)
        self.textBox = self.ui.textBox
        self.textBox.textChanged.connect(self.textChange)
        self.ui.btnDelete.clicked.connect(self.deleteSelf)
        return

    def deleteSelf(self):
        self.master.databaseHandler.deleteEntry(self)
        pass

    def textChange(self):
        self.entry.setText(self.textBox.document().toPlainText())

    def getWidget(self):
        return self.widget

    def setText(self, text):
        self.entry.setText(text)
        self.textBox.document().setPlainText(text)
        return


class DatabaseHandler(object):
    """Handles all interactions with the Database and the GUI Grid."""

    def __init__(self, master, database):
        self.master = master
        self.ui = master.ui
        self.grid = self.ui.entryView.layout()
        self.grid.setSpacing(3)
        self.entryView = self.ui.entryView
        self.database = database
        self.numColumns = 3
        self.minRowHeight = 150
        self.columnWidth = 200
        self.entryHandlers = []
        self.initEntries()
        self.updateList()
        self.resized()
        # self.grid.resizeEvent = self.resizeEvent
        return

    def addEntry(self, entry):
        self.database.addEntry(entry)
        self.entryHandlers.append(EntryHandler(self.master, entry))
        self.updateList()

    def deleteEntry(self, entryHandler):
        # self.grid.removeWidget(entryHandler.widget)
        entryHandler.widget.setParent(None)
        entryHandler.widget.deleteLater()
        self.entryHandlers.remove(entryHandler)

        self.updateList()

    def resizeEvent(self, event):
        self.resized()
        pass

    def initEntries(self):
        self.entryHandlers = [EntryHandler(e) for e in
                              self.database.getEntries()]
        return

    def updateList(self):
        for i, eH in enumerate(self.entryHandlers):
            # Magic here fills tiles consecutively left to right, then down.
            row = math.floor(i / self.numColumns)
            column = i % self.numColumns
            self.grid.addWidget(eH.widget, row, column)

        for row in range(self.grid.rowCount()):
            self.grid.setRowMinimumHeight(row, self.minRowHeight)
        return

    def resized(self):
        self.numColumns = max(math.floor(self.entryView.width() / self.columnWidth), 2)
        self.updateList()

    def reSort(self):
        if self.master.mainInterfaceHandler.sortKey == core.Database.SORT_BY_TIME_EDITED:
            self.entryHandlers.sort(key=lambda x: x.entry.timeLastEdited, reverse=True)

        elif self.master.mainInterfaceHandler.sortKey == core.Database.SORT_BY_TIME_CREATED:
            self.entryHandlers.sort(key=lambda x: x.entry.timeCreated, reverse=True)

        self.updateList()


def testing(ui, dbh):

    a = core.Entry()
    b = core.Entry()
    c = core.Entry()
    d = core.Entry()
    e = core.Entry()
    f = core.Entry()

    a.setText("Lorem Ipsum Dolor blah blah blah")
    b.setText("And that last step again.")
    c.setText("A rose by any other name would smell as sweet")
    d.setText("Whether tis' nobler to suffer the slings and\
     arrows of Outrageous misfortune")
    e.setText("The fool doth think he is wise, but the wise man knows\
        himself to be a fool.")
    f.setText("Love looks not with the eyes, but with the mind,\
And therefore is winged Cupid painted blind.")

    dbh.addEntry(a)
    # dbh.addEntry(b)
    # dbh.addEntry(c)
    # dbh.addEntry(d)
    # dbh.addEntry(e)
    # dbh.addEntry(f)
    # dbh.addEntry(a)
    # dbh.addEntry(b)
    # dbh.addEntry(c)
    # dbh.addEntry(d)
    # dbh.addEntry(e)
    # dbh.addEntry(f)
    # dbh.addEntry(a)
    # dbh.addEntry(b)
    # dbh.addEntry(c)
    # dbh.addEntry(d)
    # dbh.addEntry(e)
    # dbh.addEntry(f)
    # dbh.addEntry(a)
    # dbh.addEntry(b)
    # dbh.addEntry(c)
    # dbh.addEntry(d)
    # dbh.addEntry(e)
    # dbh.addEntry(f)
    # dbh.addEntry(a)
    # dbh.addEntry(b)
    # dbh.addEntry(c)
    # dbh.addEntry(d)
    # dbh.addEntry(e)
    # dbh.addEntry(f)
    # dbh.addEntry(a)
    # dbh.addEntry(b)
    # dbh.addEntry(c)
    # dbh.addEntry(d)
    # dbh.addEntry(e)
    # dbh.addEntry(f)
    # dbh.addEntry(a)
    # dbh.addEntry(b)
    # dbh.addEntry(c)
    # dbh.addEntry(d)
    # dbh.addEntry(e)
    # dbh.addEntry(f)


    # ui.entryView.resize(ui.entryView.width(), 100)

    # ui.centralwidget.adjustSize()

    # ah = EntryHandler(a)
    # bh = EntryHandler(b)
    # ch = EntryHandler(c)
    # dh = EntryHandler(d)

    # ui.entryGrid.layout().addWidget(ah.getWidget())
    # ui.entryGrid.layout().addWidget(bh.getWidget())
    # ui.entryGrid.layout().addWidget(ch.getWidget())
    # ui.entryGrid.layout().addWidget(dh.getWidget())

    # qDoc = QtGui.QTextDocument()
    # qDoc.setDocumentLayout(QtGui.QPlainTextDocumentLayout(qDoc))
    # qDoc.setPlainText("Testing setting text")
    # ui.entryText1.setDocument(qDoc)

if __name__ == '__main__':
    main()
