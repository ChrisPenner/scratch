#!/usr/bin/python3

import core
import xml.etree.ElementTree as ET

def databaseFromXML(xmlURL):
    tree = ET.ElementTree()
    root = tree.parse(xmlURL)
    database = core.Database()
    for entryNode in root.iter('entry'):
        entry = core.Entry()
        entry.text = entryNode.text
        attrib = entryNode.attrib
        entry.color = attrib['color']
        entry.title = attrib['title']
        entry.timeCreated = float(attrib['timeCreated'])
        entry.timeLastEdited = float(attrib['timeLastEdited'])
        database.addEntry(entry)
    return database


def databaseToXML(dest, database):
    root = ET.Element('database')
    tree = ET.ElementTree(root)
    for entry in database.entryList:
        child = ET.Element('entry')
        child.text = entry.text
        child.set('title', entry.title)
        child.set('color', entry.color)
        child.set('timeCreated', str(entry.timeCreated))
        child.set('timeLastEdited', str(entry.timeLastEdited))
        root.append(child)
    tree.write(dest)
    return
