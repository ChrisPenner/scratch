# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Sat Mar  8 18:46:19 2014
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(802, 735)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.searchBox = QtGui.QLineEdit(self.centralwidget)
        self.searchBox.setObjectName(_fromUtf8("searchBox"))
        self.horizontalLayout.addWidget(self.searchBox)
        self.btnGoSearch = QtGui.QPushButton(self.centralwidget)
        self.btnGoSearch.setObjectName(_fromUtf8("btnGoSearch"))
        self.horizontalLayout.addWidget(self.btnGoSearch)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.btnNewEntry = QtGui.QPushButton(self.centralwidget)
        self.btnNewEntry.setObjectName(_fromUtf8("btnNewEntry"))
        self.horizontalLayout_3.addWidget(self.btnNewEntry)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        self.sortSelector = QtGui.QComboBox(self.centralwidget)
        self.sortSelector.setObjectName(_fromUtf8("sortSelector"))
        self.horizontalLayout_3.addWidget(self.sortSelector)
        self.btnSort = QtGui.QPushButton(self.centralwidget)
        self.btnSort.setObjectName(_fromUtf8("btnSort"))
        self.horizontalLayout_3.addWidget(self.btnSort)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.entryScroll = QtGui.QScrollArea(self.centralwidget)
        self.entryScroll.setWidgetResizable(True)
        self.entryScroll.setObjectName(_fromUtf8("entryScroll"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 782, 594))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.entryView = QtGui.QWidget(self.scrollAreaWidgetContents)
        self.entryView.setObjectName(_fromUtf8("entryView"))
        self.gridLayout_2 = QtGui.QGridLayout(self.entryView)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.verticalLayout_2.addWidget(self.entryView)
        self.entryScroll.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_4.addWidget(self.entryScroll)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 802, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "Search:", None))
        self.btnGoSearch.setText(_translate("MainWindow", "Go!", None))
        self.btnNewEntry.setText(_translate("MainWindow", "New Entry", None))
        self.label_2.setText(_translate("MainWindow", "Sorting Method:", None))
        self.btnSort.setText(_translate("MainWindow", "Sort", None))

