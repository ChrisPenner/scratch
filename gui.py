import sys
import math
import pickle
import PyQt4
from PyQt4 import QtGui
from entrywidget import Ui_EntryWidget
import mainwindow
import core

USER_ROLE = 32

class Colors(object):
    """Dict keying core colors to QtGui colors"""
    index = {
        core.Colors.WHITE:QtGui.QColor(255, 255, 255),
        core.Colors.RED:QtGui.QColor(255, 100, 100),
        core.Colors.ORANGE:QtGui.QColor(255, 107, 48),
        core.Colors.YELLOW:QtGui.QColor(243, 236, 90),
        core.Colors.GREEN:QtGui.QColor(130, 232, 118),
        core.Colors.BLUE:QtGui.QColor(135, 232, 226),
        core.Colors.VIOLET:QtGui.QColor(235, 150, 255),
    } 

    def __init__(self):
        pass

def main():
    """Sets up and Runs App."""

    # initialize ui objects
    app = QtGui.QApplication(sys.argv)

    mw = QtGui.QMainWindow()
    ui = mainwindow.Ui_MainWindow()
    ui.setupUi(mw)

    # Create master object to hold references
    master = MasterHandler()
    master.ui = ui

    # Create Handlers:
    dbh = initDB(master, ui)
    master.databaseHandler = dbh

    interface = MainInterfaceHandler(master)
    master.mainInterfaceHandler = interface

    # Initial sorting
    master.mainInterfaceHandler.sort()

    # Show, then run app
    mw.show()
    dbh.resized()

    # testing(ui, dbh)

    app.aboutToQuit.connect(master.quit)

    sys.exit(app.exec_())
    return


def initDB(master, ui):
    """Tries to load a DB, if that fails it creates a new one."""
    try:
        db = core.load(master.saveDest)
    except (IOError, EOFError):
        db = core.Database()

    dbh = DatabaseHandler(master, db)
    # Overrides generic resizeEvent to resize Entry View IFFY
    ui.centralwidget.resizeEvent = dbh.resizeEvent

    dbh.resized()
    return dbh


class MasterHandler(object):
    """Handles references to all major objects."""

    def __init__(self):
        self.ui = None
        self.mainInterfaceHandler = None
        self.databaseHandler = None

        self.saveDest = "database.pkl"

    def quit(self):
        try:
            save(self.databaseHandler.database, self.saveDest)
        except IOError:
            print("Couldn't save, IOError")
        print("Quitting")


class MainInterfaceHandler(object):
    """Handler for the header interface and buttons."""

    def __init__(self, master):
        self.master = master
        self.ui = master.ui 
        self.sortKey = core.Database.SORT_BY_TIME_EDITED

        # Connects New Entry Button
        self.btnNewEntry = self.ui.btnNewEntry
        self.btnNewEntry.clicked.connect(self.addBlankEntry)

        # Connects sortSelector functions
        self.sortSelector = self.ui.sortSelector
        self.sortSelector.addItem("Time Edited", core.Database.SORT_BY_TIME_EDITED)
        self.sortSelector.addItem("Time Created", core.Database.SORT_BY_TIME_CREATED)
        self.sortSelector.currentIndexChanged.connect(self.sortingMethodChanged)

        # Connects sorting button
        self.btnSort = self.ui.btnSort
        self.btnSort.clicked.connect(self.sort)

        self.revSort = self.ui.revSort
        self.revSort.stateChanged.connect(self.reverseSortChanged)
        self.reverseSortChanged();

    def sort(self):
        """Tells DatabaseHandler to sort."""
        self.master.databaseHandler.reSort()

    def sortingMethodChanged(self):
        """Changes sorting method to new combobox value."""
        self.sortKey = self.sortSelector.itemData(self.sortSelector.currentIndex())

    def reverseSortChanged(self):
        self.sortInReverse = self.revSort.isChecked()


    def addBlankEntry(self):
        """Adds a new Blank Entry to the Entry View."""
        entry = core.Entry()
        entry.setText('')
        self.master.databaseHandler.addEntry(entry)
        self.master.databaseHandler.reSort()


class EntryHandler(object):
    """Handles all interactions with Entries and their Widgets."""

    def __init__(self, master, entry):
        self.master = master
        self.ui = master.ui
        self.entry = entry
        self.buildWidget()

        return

    def buildWidget(self):
        self.widget = QtGui.QWidget()
        self.ui = Ui_EntryWidget()
        self.ui.setupUi(self.widget)
        self.textBox = self.ui.textBox
        self.setText(self.entry.getText())
        self.textBox.textChanged.connect(self.textChange)

        self.titleText = self.ui.titleText
        self.setTitle()
        self.titleText.textChanged.connect(self.titleChange)

        self.ui.btnDelete.clicked.connect(self.deleteSelf)

        self.colorPicker = self.ui.colorPicker
        self.initColorPicker()
        self.changeColor();
        self.colorPicker.currentIndexChanged.connect(self.changeColor)
        return

    def initColorPicker(self):
        #TODO: Set colorPicker to the entry's current color
        self.colorPicker.addItem("White", core.Colors.WHITE)
        self.colorPicker.addItem("Red", core.Colors.RED)
        self.colorPicker.addItem("Orange", core.Colors.ORANGE)
        self.colorPicker.addItem("Yellow", core.Colors.YELLOW)
        self.colorPicker.addItem("Green", core.Colors.GREEN)
        self.colorPicker.addItem("Blue", core.Colors.BLUE)
        self.colorPicker.addItem("Violet", core.Colors.VIOLET)
        currentIndex = self.colorPicker.findData(self.entry.color, USER_ROLE)
        self.colorPicker.setCurrentIndex(currentIndex)

    def changeColor(self):
        """Changes color of textBox's background to match colorPicker"""
        color = self.colorPicker.itemData(self.colorPicker.currentIndex())
        QTColor = Colors.index[color]
        palette = self.textBox.palette()
        palette.setColor(QtGui.QPalette.Base, QTColor );
        self.textBox.setPalette(palette);
        self.entry.color = color


    def deleteSelf(self):
        self.master.databaseHandler.deleteEntry(self)

    def setTitle(self):
        self.titleText.selectAll()
        self.titleText.insert(self.entry.getTitle())

    def titleChange(self):
        self.entry.setTitle(self.titleText.text())

    def textChange(self):
        self.entry.setText(self.textBox.document().toPlainText())

    def getWidget(self):
        return self.widget

    def setText(self, text):
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
        self.minRowHeight = 200
        self.columnWidth = 200
        self.entryHandlers = []
        self.initEntries()
        self.updateList()
        self.resized()
        return

    def addEntry(self, entry):
        """Adds entry to EntryView and database."""
        self.database.addEntry(entry)
        self.entryHandlers.append(EntryHandler(self.master, entry))
        self.updateList()

    def deleteEntry(self, entryHandler):
        """Deletes 'entryHandler'."""
        # self.grid.removeWidget(entryHandler.widget)
        # IFFY, might need to delete signal handlers
        entryHandler.widget.setParent(None)
        entryHandler.widget.deleteLater()
        self.entryHandlers.remove(entryHandler)
        self.database.removeEntry(entryHandler.entry)
        self.updateList()

    def resizeEvent(self, event):
        """Resizes elements when user resizes window."""
        self.resized()

    def initEntries(self):
        """Adds handlers for all entries in database."""
        self.entryHandlers = [EntryHandler(self.master, e) for e in
                              self.database.getEntries()]
        return

    def updateList(self):
        """Reprints widgets to itemView. """
        for i, eH in enumerate(self.entryHandlers):
            # Magic here fills tiles consecutively left to right, then down.
            row = math.floor(i / self.numColumns)
            column = i % self.numColumns
            self.grid.addWidget(eH.widget, row, column)

        for row in range(self.grid.rowCount()):
            self.grid.setRowMinimumHeight(row, self.minRowHeight)

        # for eh in self.entryHandlers:
        #     print(eh.entry.timeLastEdited)
        return

    def resized(self):
        """Resizes columns and rows to match window size."""
        self.numColumns = max(math.floor(self.entryView.width() / self.columnWidth), 2)
        self.updateList()

    def reSort(self):
        """Sorts Entries by sortKey."""
        revSort = self.master.mainInterfaceHandler.sortInReverse
        if self.master.mainInterfaceHandler.sortKey == core.Database.SORT_BY_TIME_EDITED:
            self.entryHandlers.sort(key=lambda x: x.entry.timeLastEdited, reverse=revSort)

        elif self.master.mainInterfaceHandler.sortKey == core.Database.SORT_BY_TIME_CREATED:
            self.entryHandlers.sort(key=lambda x: x.entry.timeCreated, reverse=revSort)

        self.updateList()


def save(obj, dest):
    with open(dest, 'wb') as f:
        pickle.dump(obj, f)

def load(dest):
    with open(dest, 'rb') as f:
        obj = pickle.load(f)
        return obj

if __name__ == '__main__':
    main()
