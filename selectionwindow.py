from PyQt5.QtCore import Qt, QSize, QDate, QVariant, QEvent
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTreeWidgetItem, QDialogButtonBox, QDialog, QWidget, QHeaderView, QMessageBox

import roles
from models import Movie, Type, Actor, Category
from ui_modules.selectionwindow import Ui_selectionWindow


class SelectionWindow(QDialog, Ui_selectionWindow):

    def __init__(self, parent: QWidget, mode: roles.WindowSelectionRoles = -1):
        super(SelectionWindow, self).__init__(parent)
        self.setupUi(self)

        # set the icons for the buttonbox
        self.buttonBox.button(QDialogButtonBox.Ok).setIcon(QIcon(":/icons/add.png"))
        self.buttonBox.button(QDialogButtonBox.Ok).setIconSize(QSize(16, 16))
        self.buttonBox.button(QDialogButtonBox.Cancel).setIcon(QIcon(":/icons/cancel.png"))
        self.buttonBox.button(QDialogButtonBox.Cancel).setIconSize(QSize(16, 16))

        self.treeWidget.header().setSectionResizeMode(QHeaderView.Stretch)

        if mode == roles.WindowSelectionRoles.ACTOR.value:
            self.treeWidget.headerItem().setText(0, "Schauspieler")
            self.setWindowTitle("Schauspieler hinzufügen")
            for actor in Actor.getAllActors():
                item = QTreeWidgetItem(self.treeWidget)
                item.setText(0, "{}, {}".format(actor.name, actor.prename))
                item.setData(0, roles.UserRoles.ACTOR_ID.value, actor.id)
                self.treeWidget.addTopLevelItem(item)

        elif mode == roles.WindowSelectionRoles.MOVIE.value:
            self.treeWidget.headerItem().setText(0, "Filme")
            self.setWindowTitle("Film hinzufügen")
            for movie in Movie.getAllMovies():
                item = QTreeWidgetItem(self.treeWidget)
                item.setText(0, movie.title)
                item.setData(0, roles.UserRoles.MOVIE_ID.value, movie.id)
                self.treeWidget.addTopLevelItem(item)

        elif mode == roles.WindowSelectionRoles.CATEGORY.value:
            self.treeWidget.headerItem().setText(0, "Kategorie")
            self.setWindowTitle("Kategorie hinzufügen")
            for category in Category.getAllCategories():
                item = QTreeWidgetItem(self.treeWidget)
                item.setText(0, category.name)
                item.setData(0, roles.UserRoles.CATEGORY_ID.value, category.id)
                self.treeWidget.addTopLevelItem(item)

        else:
            QMessageBox.critical(self, "Internal Error", "Selection Window was created with unknown mode", QMessageBox.Ok)

    def getSelectedIds(self, role: roles.UserRoles):
        ret = list()
        for item in self.treeWidget.selectedItems():
            if not item.data(0, role.value) == None:
                ret.append(int(item.data(0, role.value)))
        return ret

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            self.retranslateUi(self)
        super().changeEvent(event)