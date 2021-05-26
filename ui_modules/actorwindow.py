# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\actorwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_actorWindow(object):
    def setupUi(self, actorWindow):
        actorWindow.setObjectName("actorWindow")
        actorWindow.resize(413, 556)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(actorWindow.sizePolicy().hasHeightForWidth())
        actorWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        actorWindow.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(actorWindow)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.trwMovieList = QtWidgets.QTreeWidget(actorWindow)
        self.trwMovieList.setAlternatingRowColors(True)
        self.trwMovieList.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.trwMovieList.setIndentation(5)
        self.trwMovieList.setObjectName("trwMovieList")
        self.gridLayout.addWidget(self.trwMovieList, 1, 0, 1, 4)
        self.ledPrename = QtWidgets.QLineEdit(actorWindow)
        self.ledPrename.setObjectName("ledPrename")
        self.gridLayout.addWidget(self.ledPrename, 0, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(actorWindow)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.ledName = QtWidgets.QLineEdit(actorWindow)
        self.ledName.setObjectName("ledName")
        self.gridLayout.addWidget(self.ledName, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(actorWindow)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(15, -1, -1, -1)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.movieAdd = QtWidgets.QToolButton(actorWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.movieAdd.setIcon(icon1)
        self.movieAdd.setObjectName("movieAdd")
        self.horizontalLayout_2.addWidget(self.movieAdd, 0, QtCore.Qt.AlignRight)
        self.movieRemove = QtWidgets.QToolButton(actorWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.movieRemove.setIcon(icon2)
        self.movieRemove.setObjectName("movieRemove")
        self.horizontalLayout_2.addWidget(self.movieRemove)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 3, 1, 1)
        self.gridLayout.setRowStretch(1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.line = QtWidgets.QFrame(actorWindow)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.buttonBox = QtWidgets.QDialogButtonBox(actorWindow)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(actorWindow)
        self.buttonBox.accepted.connect(actorWindow.accept)
        self.buttonBox.rejected.connect(actorWindow.reject)
        QtCore.QMetaObject.connectSlotsByName(actorWindow)
        actorWindow.setTabOrder(self.ledName, self.ledPrename)
        actorWindow.setTabOrder(self.ledPrename, self.trwMovieList)
        actorWindow.setTabOrder(self.trwMovieList, self.movieAdd)
        actorWindow.setTabOrder(self.movieAdd, self.movieRemove)

    def retranslateUi(self, actorWindow):
        _translate = QtCore.QCoreApplication.translate
        actorWindow.setWindowTitle(_translate("actorWindow", "Schauspieler anlegen"))
        self.trwMovieList.headerItem().setText(0, _translate("actorWindow", "Filme"))
        self.label_2.setText(_translate("actorWindow", "Vorname:"))
        self.label.setText(_translate("actorWindow", "Name:"))
        self.movieAdd.setText(_translate("actorWindow", "..."))
        self.movieRemove.setText(_translate("actorWindow", "..."))
from ui_modules import resources_rc
