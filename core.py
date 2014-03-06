#!/usr/bin/python3
import time


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
        self.text = ''
        return

    def edited(self):
        self.timeLastEdited = time.localtime()

    def setText(self, text):
        self.text = text
        self.edited()

    def getText(self):
        return self.text

    def getTimeLastEdited(self):
        return self.timeLastEdited

    def getTimeCreated(self):
        return self.timeCreated
