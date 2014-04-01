#!/usr/bin/python3
import time
import pickle


class Colors(object):
    """docstring for Colors"""
    WHITE = 'white'
    RED = 'red'
    ORANGE = 'orange'
    YELLOW = 'yellow'
    GREEN = 'green'
    BLUE = 'blue'
    VIOLET = 'violet'

    def __init__(self):
        pass


class Database(object):
    """Holds information about the top-level database."""

    # Set sortKey Constants
    SORT_BY_TIME_EDITED = "time_edited"
    SORT_BY_TIME_CREATED = "time_created"

    def __init__(self):
        """Initializes new Database instance."""
        self.entryList = []
        self.count = 0
        self.sortKey = Database.SORT_BY_TIME_EDITED
        return

    def addEntry(self, entry):
        self.entryList.append(entry)
        self.reSort()

    def removeEntry(self, entry):
        self.entryList.remove(entry)

    def getEntries(self):
        return self.entryList[:]

    def reSort(self):
        if self.sortKey == self.SORT_BY_TIME_EDITED:
            self.entryList.sort(key=lambda x: x.timeLastEdited)

        elif self.sortKey == self.SORT_BY_TIME_CREATED:
            self.entryList.sort(key=lambda x: x.timeLastEdited, reverse=True)


class Entry(object):
    """Holds information about an entry instance."""

    def __init__(self):
        """Initializes new Entry instance."""
        self.timeCreated = time.localtime()
        self.timeLastEdited = time.localtime()
        self.title = ''
        self.text = ''
        self.color = Colors.WHITE
        return

    def edited(self):
        self.timeLastEdited = time.localtime()

    def setText(self, text):
        self.text = text
        self.edited()

    def setTitle(self,text):
        self.title = text
        self.edited()

    def getText(self):
        return self.text

    def getTitle(self):
        return self.title

    def getTimeLastEdited(self):
        return self.timeLastEdited

    def getTimeCreated(self):
        return self.timeCreated

def save(obj, dest):
    with open(dest, 'wb') as f:
        pickle.dump(obj, f)

def load(dest):
    with open(dest, 'rb') as f:
        obj = pickle.load(f)
        return obj
