# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'entrywidget.ui'
#
# Created: Sat Mar  8 17:15:26 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_EntryWidget(object):
    def setupUi(self, EntryWidget):
        EntryWidget.setObjectName(_fromUtf8("EntryWidget"))
        EntryWidget.resize(274, 245)
        self.verticalLayout = QtGui.QVBoxLayout(EntryWidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnDelete = QtGui.QToolButton(EntryWidget)
        self.btnDelete.setObjectName(_fromUtf8("btnDelete"))
        self.horizontalLayout.addWidget(self.btnDelete)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.colorPicker = QtGui.QComboBox(EntryWidget)
        self.colorPicker.setEditable(False)
        self.colorPicker.setObjectName(_fromUtf8("colorPicker"))
        self.horizontalLayout.addWidget(self.colorPicker)
        self.selectBox = QtGui.QCheckBox(EntryWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectBox.sizePolicy().hasHeightForWidth())
        self.selectBox.setSizePolicy(sizePolicy)
        self.selectBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.selectBox.setText(_fromUtf8(""))
        self.selectBox.setObjectName(_fromUtf8("selectBox"))
        self.horizontalLayout.addWidget(self.selectBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textBox = QtGui.QPlainTextEdit(EntryWidget)
        self.textBox.setObjectName(_fromUtf8("textBox"))
        self.verticalLayout.addWidget(self.textBox)

        self.retranslateUi(EntryWidget)
        QtCore.QMetaObject.connectSlotsByName(EntryWidget)

    def retranslateUi(self, EntryWidget):
        EntryWidget.setWindowTitle(_translate("EntryWidget", "Form", None))
        self.btnDelete.setText(_translate("EntryWidget", "x", None))

