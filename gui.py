import sys
import math
import PyQt4
from PyQt4 import QtGui
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

    testing(ui)

    mw.show()
    sys.exit(app.exec_())
    return


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
        self.widget.setLayout(QtGui.QVBoxLayout())

        blankDoc = QtGui.QTextDocument()
        blankDoc.setDocumentLayout(QtGui.QPlainTextDocumentLayout(blankDoc))
        self.textBox = QtGui.QPlainTextEdit()
        self.textBox.setDocument(blankDoc)

        self.widget.layout().addWidget(self.textBox)
        return

    def getWidget(self):
        return self.widget

    def setText(self, text):
        self.entry.setText(text)
        self.textBox.document().setPlainText(text)
        return


class DatabaseHandler(object):
    """Handles all interactions with the Database and the GUI Grid."""

    def __init__(self, database, grid):
        self.database = database
        self.grid = grid
        self.numColumns = 3
        self.entryHandlers = []
        self.initEntries()
        self.updateList()
        return

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
        return


def testing(ui):
    db = core.Database()

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

    db.addEntry(a)
    db.addEntry(b)
    db.addEntry(c)
    db.addEntry(d)
    db.addEntry(e)
    db.addEntry(f)

    dbh = DatabaseHandler(db, ui.entryGrid)

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
