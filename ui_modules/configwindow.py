# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/configwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_configWindow(object):
    def setupUi(self, configWindow):
        configWindow.setObjectName("configWindow")
        configWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        configWindow.resize(421, 363)
        configWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        configWindow.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(configWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(configWindow)
        self.label.setMinimumSize(QtCore.QSize(100, 0))
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.cbLanguage = QtWidgets.QComboBox(configWindow)
        self.cbLanguage.setObjectName("cbLanguage")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.cbLanguage)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(configWindow)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.verticalLayout.setStretch(0, 1)

        self.retranslateUi(configWindow)
        self.buttonBox.accepted.connect(configWindow.accept)
        self.buttonBox.rejected.connect(configWindow.reject)
        QtCore.QMetaObject.connectSlotsByName(configWindow)

    def retranslateUi(self, configWindow):
        _translate = QtCore.QCoreApplication.translate
        configWindow.setWindowTitle(_translate("configWindow", "Properties"))
        self.label.setText(_translate("configWindow", "Language"))
