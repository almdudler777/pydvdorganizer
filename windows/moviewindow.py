from PyQt5.QtCore import Qt, QSize, QDate, QVariant, QEvent
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTreeWidgetItem, QDialogButtonBox, QDialog, QWidget, QMessageBox

import roles
from models import Movie, Type, Actor, Category
from .selectionwindow import SelectionWindow
from ui_modules.moviewindow import Ui_movieWindow


class MovieWindow(QDialog, Ui_movieWindow):

    def __init__(self, parent: QWidget, movieId: int = 0):
        super(MovieWindow, self).__init__(parent)
        self.setupUi(self)

        # connect
        self.schauspielerTree.itemSelectionChanged.connect(self.evt_schauspielerTree_itemSelectionChanged)
        self.kategorieTree.itemSelectionChanged.connect(self.evt_kategorieTree_itemSelectionChanged)
        self.SchauspielerRemove.clicked.connect(self.evt_schauspielerremove_clicked)
        self.kategorieRemove.clicked.connect(self.evt_kategorieRemove_clicked)
        self.kategorieAdd.clicked.connect(self.evt_KategorieAdd_clicked)
        self.schauspielerAdd.clicked.connect(self.evt_SchauspielerAdd_clicked)
        self.accepted.connect(self.evt_movieWindow_accepted)

        # set the icons for the buttonbox
        self.buttonBox.button(QDialogButtonBox.Ok).setIcon(QIcon(":/icons/film_save.png"))
        self.buttonBox.button(QDialogButtonBox.Ok).setIconSize(QSize(16, 16))
        self.buttonBox.button(QDialogButtonBox.Cancel).setIcon(QIcon(":/icons/cancel.png"))
        self.buttonBox.button(QDialogButtonBox.Cancel).setIconSize(QSize(16, 16))

        # just to make sure remove buttons are disabled from the startup
        self.evt_schauspielerTree_itemSelectionChanged()
        self.evt_kategorieTree_itemSelectionChanged()

        self._movieId = movieId

        # fill type combobox
        for type in Type.getAllTypes():
            self.typ.addItem(type.name, QVariant(type.id))

        if movieId > 0:  # we're going to edit a movie that already exists
            self.setWindowTitle(self.tr("Update movie"))
            mov = Movie.getMovieById(movieId)
            self.titel.setText(mov.title)
            self.laenge.setValue(mov.length)
            self.preis.setValue(mov.cost)
            self.medien.setValue(mov.mediums)
            self.usk.setCurrentIndex(self.usk.findText(str(mov.rated), Qt.MatchStartsWith))

            for actor in mov.getActors():
                item = QTreeWidgetItem(self.schauspielerTree)
                item.setText(0, "{} {}".format(
                    actor.prename, actor.name
                ))
                item.setData(0, roles.UserRoles.ACTOR_ID.value, actor.id)
                self.schauspielerTree.addTopLevelItem(item)

            for category in mov.getCategories():
                item = QTreeWidgetItem(self.kategorieTree)
                item.setText(0, category.name)
                item.setData(0, roles.UserRoles.CATEGORY_ID.value, category.id)
                self.kategorieTree.addTopLevelItem(item)

            for i in range(0, self.typ.count()):
                if int(self.typ.itemData(i)) == mov.type.id:
                    self.typ.setCurrentIndex(i)

        else:  # we're going to create a new movie
            self.setWindowTitle(self.tr("Create new movie"))
            # set the date fields to a date nearby
            self.gekauft.setDate(QDate.currentDate())
            self.release.setDate(QDate.currentDate())

    def evt_kategorieTree_itemSelectionChanged(self):
        if len(self.kategorieTree.selectedItems()) >= 1:
            self.kategorieRemove.setEnabled(True)
        else:
            self.kategorieRemove.setEnabled(False)

    def evt_schauspielerTree_itemSelectionChanged(self):
        if len(self.schauspielerTree.selectedItems()) >= 1:
            self.SchauspielerRemove.setEnabled(True)
        else:
            self.SchauspielerRemove.setEnabled(False)

    def evt_kategorieRemove_clicked(self):
        for item in self.kategorieTree.selectedItems():
            self.kategorieTree.invisibleRootItem().removeChild(item)

    def evt_schauspielerremove_clicked(self):
        for item in self.schauspielerTree.selectedItems():
            self.schauspielerTree.invisibleRootItem().removeChild(item)

    def evt_SchauspielerAdd_clicked(self):
        w = SelectionWindow(self, roles.WindowSelectionRoles.ACTOR)
        if w.exec_() == QDialog.Accepted:
            for id in w.getSelectedIds(roles.UserRoles.ACTOR_ID):
                found = False
                for i in range(0, self.schauspielerTree.topLevelItemCount()):
                    if self.schauspielerTree.topLevelItem(i).data(0, roles.UserRoles.ACTOR_ID.value) == id:
                        found = True
                        break

                if not found:
                    item = QTreeWidgetItem(self.schauspielerTree)
                    actor = Actor.getActorById(id)
                    item.setText(0, "{} {}".format(actor.prename, actor.name))
                    item.setData(0, roles.UserRoles.ACTOR_ID.value, actor.id)
                    self.schauspielerTree.addTopLevelItem(item)

    def evt_KategorieAdd_clicked(self):
        w = SelectionWindow(self, roles.WindowSelectionRoles.CATEGORY)
        if w.exec_() == QDialog.Accepted:
            for id in w.getSelectedIds(roles.UserRoles.CATEGORY_ID):
                found = False
                for i in range(0, self.kategorieTree.topLevelItemCount()):
                    if self.kategorieTree.topLevelItem(i).data(0, roles.UserRoles.CATEGORY_ID.value) == id:
                        found = True
                        break
                if not found:
                    item = QTreeWidgetItem(self.kategorieTree)
                    category = Category.getCategoryById(id)
                    item.setText(0, category.name)
                    item.setData(0, roles.UserRoles.CATEGORY_ID.value, category.id)
                    self.kategorieTree.addTopLevelItem(item)

    def evt_movieWindow_accepted(self):
        mov = Movie(
            id=self._movieId,
            cost=self.preis.value(),
            length=self.laenge.value(),
            mediums=self.medien.value(),
            rated=int(self.usk.currentText()),
            title=self.titel.text(),
        )

        mov.type = Type.getTypeById(int(self.typ.currentData()))

        actorIds = list()
        for i in range(0, self.schauspielerTree.topLevelItemCount()):
            actorIds.append(int(self.schauspielerTree.topLevelItem(i).data(0,roles.UserRoles.ACTOR_ID.value)))
        mov.setActors(actorIds)

        categoryIds = list()
        for i in range(0, self.kategorieTree.topLevelItemCount()):
            categoryIds.append(int(self.kategorieTree.topLevelItem(i).data(0, roles.UserRoles.CATEGORY_ID.value)))
        mov.setCategories(categoryIds)

        mov.save()

    def done(self, result):
        if result == QDialog.Accepted:
            if self.titel.text() == "":
                QMessageBox.warning(self, "Error", "Please enter a title", QMessageBox.Ok)
                return

        super().done(result)

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            self.retranslateUi(self)
        super().changeEvent(event)