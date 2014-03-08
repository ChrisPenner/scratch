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

    mwHandler = mainWindowHandler(mw, ui)

    mwHandler.initMainWindow()

    dbh = initDB(ui)
    mw.show()
    dbh.resized()

    testing(ui, dbh)

    sys.exit(app.exec_())
    return


def initDB(ui):
    db = core.Database()
    grid = QtGui.QGridLayout()
    ui.entryView.setLayout(grid)

    # ui.entryView.setFixedHeight(400)

    dbh = DatabaseHandler(db, ui.entryView)
    ui.centralwidget.resizeEvent = dbh.resizeEvent

    dbh.resized()
    return dbh


class mainWindowHandler(object):
    """Main event handler for ui"""

    def __init__(self, mainWindow, ui):
        super(mainWindowHandler, self).__init__()

        self.mw = mainWindow
        self.ui = ui
        # self.btnEditEntry = ui.btnEditEntry

    def initMainWindow(self):
        """ Sets up main GUI window. """
        pass


class EntryHandler(object):
    """Handles all interactions with Entries and their Widgets."""

    def __init__(self, entry):
        self.entry = entry
        self.buildWidget()

        self.setText(entry.getText())
        return

    def buildWidget(self):
        self.widget = QtGui.QWidget()
        self.ui = Ui_EntryWidget()
        self.ui.setupUi(self.widget)
        self.textBox = self.ui.textBox
        return

    def getWidget(self):
        return self.widget

    def setText(self, text):
        self.entry.setText(text)
        self.textBox.document().setPlainText(text)
        return


class DatabaseHandler(object):
    """Handles all interactions with the Database and the GUI Grid."""

    def __init__(self, database, entryView):
        self.grid = entryView.layout()
        self.grid.setSpacing(3)
        self.entryView = entryView
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
        self.entryHandlers.append(EntryHandler(entry))
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
            self.grid.setRowMinimumHeight(row, self.minRowHeight)
        return

    def resized(self):
        print("resized")
        self.numColumns = max(math.floor(self.entryView.width() / self.columnWidth), 2)
        self.updateList()


def resizeEvent(event):
    print("yup")


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
    dbh.addEntry(b)
    dbh.addEntry(c)
    dbh.addEntry(d)
    dbh.addEntry(e)
    dbh.addEntry(f)
    dbh.addEntry(a)
    dbh.addEntry(b)
    dbh.addEntry(c)
    dbh.addEntry(d)
    dbh.addEntry(e)
    dbh.addEntry(f)
    dbh.addEntry(a)
    dbh.addEntry(b)
    dbh.addEntry(c)
    dbh.addEntry(d)
    dbh.addEntry(e)
    dbh.addEntry(f)
    dbh.addEntry(a)
    dbh.addEntry(b)
    dbh.addEntry(c)
    dbh.addEntry(d)
    dbh.addEntry(e)
    dbh.addEntry(f)
    dbh.addEntry(a)
    dbh.addEntry(b)
    dbh.addEntry(c)
    dbh.addEntry(d)
    dbh.addEntry(e)
    dbh.addEntry(f)
    dbh.addEntry(a)
    dbh.addEntry(b)
    dbh.addEntry(c)
    dbh.addEntry(d)
    dbh.addEntry(e)
    dbh.addEntry(f)
    dbh.addEntry(a)
    dbh.addEntry(b)
    dbh.addEntry(c)
    dbh.addEntry(d)
    dbh.addEntry(e)
    dbh.addEntry(f)


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
