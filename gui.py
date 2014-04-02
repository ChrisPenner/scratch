#!/usr/bin/python3
import sys
import os
import math
import time
import pickle
import PyQt4
from PyQt4 import QtGui, QtCore
from entrywidget import Ui_EntryWidget
import mainwindow
import core
import xmlparser

# Constants
USER_ROLE = 32
DEST = "database.xml"
BACKUP_XML_DEST = ".~database.xml"


class Colors(object):
    """Dict keying core colors to QtGui colors for reference"""
    index = {
        core.Colors.WHITE: QtGui.QColor(255, 255, 255),
        core.Colors.RED: QtGui.QColor(255, 100, 100),
        core.Colors.ORANGE: QtGui.QColor(255, 107, 48),
        core.Colors.YELLOW: QtGui.QColor(243, 236, 90),
        core.Colors.GREEN: QtGui.QColor(130, 232, 118),
        core.Colors.BLUE: QtGui.QColor(135, 232, 226),
        core.Colors.VIOLET: QtGui.QColor(235, 150, 255),
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
    master = MasterHandler(ui)

    # Create Handlers:
    dbh = initDB(master)

    interface = MainInterfaceHandler(master)

    # Initial sorting
    master.mainInterfaceHandler.sort()

    # Sets up and starts Backup timer:
    backupTimer = QtCore.QTimer()
    backupTimer.timeout.connect(master.backup)
    # Backs up every minute
    backupTimer.start(30000)

    # Show, then run app
    mw.show()
    dbh.resized()

    app.aboutToQuit.connect(master.quit)

    sys.exit(app.exec_())
    return


def initDB(master):
    """Tries to load a DB, if that fails it creates a new one."""
    if os.path.isfile(BACKUP_XML_DEST):
        try:
            db = xmlparser.databaseFromXML(BACKUP_XML_DEST)
        except:
            try:
                db = xmlparser.databaseFromXML(DEST)
            except (IOError, EOFError):
                db = core.Database()
                print("No save found, creating new one") 
    else:
        try:
            # Legacy load from .pkl
            # db = core.load(master.saveDest)
            db = xmlparser.databaseFromXML(DEST)
        except (IOError, EOFError):
            db = core.Database()
            print("No save found, creating new one")

    dbh = DatabaseHandler(master, db)
    # Overrides generic resizeEvent to resize Entry View IFFY
    master.ui.centralwidget.resizeEvent = dbh.resizeEvent

    dbh.resized()
    master.databaseHandler = dbh
    return dbh


class MasterHandler(object):
    """Handles references to all major objects."""

    def __init__(self, ui):
        self.ui = ui
        self.mainInterfaceHandler = None
        self.databaseHandler = None

        self.saveDest = "database.pkl"

    def quit(self):
        try:
            # save(self.databaseHandler.database, self.saveDest)
            writeXML(DEST, self.databaseHandler.database)
            if os.path.isfile(BACKUP_XML_DEST):
                os.remove(BACKUP_XML_DEST)
        except IOError:
            print("Couldn't save, IOError")

        print("Quitting")

    def backup(self):
        writeXML(BACKUP_XML_DEST, self.databaseHandler.database)
        print("Backed up at", time.asctime())


class MainInterfaceHandler(object):
    """Handler for the header interface and buttons."""

    def __init__(self, master):
        self.master = master
        self.ui = master.ui
        master.mainInterfaceHandler = self


        # Connects New Entry Button
        self.btnNewEntry = self.ui.btnNewEntry
        self.btnNewEntry.clicked.connect(self.addBlankEntry)

        # Connects Searching
        self.searchBox = self.ui.searchBox
        self.searchBox.textEdited.connect(self.search)

        # Connects sortSelector functions
        self.sortKey = core.Database.SORT_BY_TIME_EDITED
        self.sortSelector = self.ui.sortSelector
        self.initSortSelector()

        # Connects sorting buttons
        self.btnSort = self.ui.btnSort
        self.btnSort.clicked.connect(self.sort)

        self.revSort = self.ui.revSort
        self.revSort.stateChanged.connect(self.reverseSortChanged)

        # init revSort value
        self.reverseSortChanged()

    def initSortSelector(self):
        """Adds values to sorting combobox"""
        self.sortSelector.addItem(
            "Time Edited", core.Database.SORT_BY_TIME_EDITED)
        self.sortSelector.addItem(
            "Time Created", core.Database.SORT_BY_TIME_CREATED)
        self.sortSelector.currentIndexChanged.connect(
            self.sortingMethodChanged)
        return

    def sort(self):
        """Tells DatabaseHandler to sort."""
        self.master.databaseHandler.sort()
        return

    def sortingMethodChanged(self):
        """Changes sorting method to new combobox value."""
        self.sortKey = self.sortSelector.itemData(
            self.sortSelector.currentIndex())

    def reverseSortChanged(self):
        """Swaps reverse sort value when box is ticked."""
        self.sortInReverse = not self.revSort.isChecked()

    def search(self):
        """Searches text of all entries and displays valid matches."""
        if self.searchBox.text() == '':
            self.master.databaseHandler.visibleEntries = (
                self.master.databaseHandler.entryHandlers[:])
            for eh in self.master.databaseHandler.entryHandlers:
                eh.textBox.moveCursor(QtGui.QTextCursor.Start)
            self.sort()
            return

        searchTerms = self.searchBox.text().split(' ')
        if '' in searchTerms:
            searchTerms.remove('')

        results = []
        for eh in self.master.databaseHandler.entryHandlers:
            # Search Prioritizes based on number of matches
            matches = 0
            for term in searchTerms:
                # Cursor must be at start of text to match anything.
                eh.textBox.moveCursor(QtGui.QTextCursor.Start)

                if eh.textBox.find(term) or (term.lower() in eh.titleText.text().lower()):
                        matches += 1

            if matches > 0:
                results.append((matches, eh))

        results.sort(key=lambda x:x[0], reverse=True)

        self.master.databaseHandler.visibleEntries = [x[1] for x in results]
        self.master.databaseHandler.updateList()

    def addBlankEntry(self):
        """Adds a new Blank Entry to the Entry View."""
        entry = core.Entry()
        self.master.databaseHandler.addEntry(entry)
        self.sort()


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
        self.changeColor()
        self.colorPicker.currentIndexChanged.connect(
            self.changeColor)
        return

    def initColorPicker(self):
        self.colorPicker.addItem("White", core.Colors.WHITE)
        self.colorPicker.addItem("Red", core.Colors.RED)
        self.colorPicker.addItem("Orange", core.Colors.ORANGE)
        self.colorPicker.addItem("Yellow", core.Colors.YELLOW)
        self.colorPicker.addItem("Green", core.Colors.GREEN)
        self.colorPicker.addItem("Blue", core.Colors.BLUE)
        self.colorPicker.addItem("Violet", core.Colors.VIOLET)
        # Set colorPicker to entry's color
        currentIndex = self.colorPicker.findData(self.entry.color, USER_ROLE)
        self.colorPicker.setCurrentIndex(currentIndex)
        return

    def changeColor(self):
        """Changes color of textBox's background to match colorPicker"""
        color = self.colorPicker.itemData(self.colorPicker.currentIndex())
        QTColor = Colors.index[color]
        palette = self.textBox.palette()
        palette.setColor(QtGui.QPalette.Base, QTColor)
        self.textBox.setPalette(palette)
        self.entry.color = color
        return

    def deleteSelf(self):
        self.master.databaseHandler.deleteEntry(self)
        return

    def setTitle(self):
        self.titleText.clear()
        self.titleText.insert(self.entry.getTitle())
        return

    def titleChange(self):
        self.entry.setTitle(self.titleText.text())
        return

    def textChange(self):
        self.entry.setText(self.textBox.document().toPlainText())
        return

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
        self.visibleEntries = []
        self.initEntries()
        self.updateList()
        self.resized()
        return

    def addEntry(self, entry):
        """Adds entry to EntryView and database."""
        self.database.addEntry(entry)
        eh = EntryHandler(self.master, entry)
        self.entryHandlers.append(eh)
        if eh not in self.visibleEntries:
            self.visibleEntries.append(eh)
        self.updateList()
        return

    def deleteEntry(self, entryHandler):
        """Deletes 'entryHandler'."""
        # self.grid.removeWidget(entryHandler.widget)
        # IFFY, might need to delete signal handlers
        entryHandler.widget.setParent(None)
        entryHandler.widget.deleteLater()
        self.entryHandlers.remove(entryHandler)
        if entryHandler in self.visibleEntries:
            self.visibleEntries.remove(entryHandler)
        self.database.removeEntry(entryHandler.entry)
        self.updateList()
        return

    def initEntries(self):
        """Adds handlers for all entries in database."""
        self.entryHandlers = [EntryHandler(self.master, e) for e in self.database.getEntries()]
        self.visibleEntries = self.entryHandlers[:]
        return

    def updateList(self):
        """Reprints widgets to itemView. """
        for eH in self.entryHandlers:
            eH.widget.setParent(None)

        for i, eH in enumerate(self.visibleEntries):
            # Magic here fills tiles consecutively left to right, then down.
            row = math.floor(i / self.numColumns)
            column = i % self.numColumns
            self.grid.addWidget(eH.widget, row, column)

        for row in range(self.grid.rowCount()):
            self.grid.setRowMinimumHeight(row, self.minRowHeight)
        return

    def resizeEvent(self, event):
        """Resizes elements when user resizes window."""
        self.resized()
        return

    def resized(self):
        """Resizes columns and rows to match window size."""
        self.numColumns = max(
            math.floor(self.entryView.width() / self.columnWidth), 2)
        self.updateList()
        return

    def sort(self):
        """Sorts Entries by sortKey."""
        revSort = self.master.mainInterfaceHandler.sortInReverse
        if (self.master.mainInterfaceHandler.sortKey ==
                core.Database.SORT_BY_TIME_EDITED):
            self.visibleEntries.sort(key=lambda x:\
                x.entry.timeLastEdited, reverse=revSort)

        elif (self.master.mainInterfaceHandler.sortKey ==
                core.Database.SORT_BY_TIME_CREATED):
            self.visibleEntries.sort(key=lambda x:\
                x.entry.timeCreated, reverse=revSort)
        self.updateList()
        return


def save(obj, dest):
    with open(dest, 'wb') as f:
        pickle.dump(obj, f)
        return


def load(dest):
    with open(dest, 'rb') as f:
        obj = pickle.load(f)
        return obj

def writeXML(dest, database):
    xmlparser.databaseToXML(dest, database)

if __name__ == '__main__':
    main()
