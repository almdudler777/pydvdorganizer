from PyQt5.QtCore import Qt, QSize, QDate, QVariant
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTreeWidgetItem, QDialogButtonBox, QDialog, QWidget, QMessageBox

import roles
from models import Movie, Type, Actor, Category
from .selectionwindow import SelectionWindow
from ui_modules.actorwindow import Ui_actorWindow


class ActorWindow(QDialog, Ui_actorWindow):

    def __init__(self, parent: QWidget, actorId: int = 0):
        super(ActorWindow, self).__init__(parent)
        self.setupUi(self)

        # connect signals
        self.movieAdd.clicked.connect(self.evtMovieAdd_clicked)
        self.movieRemove.clicked.connect(self.evtMovieRemove_clicked)
        self.trwMovieList.itemSelectionChanged.connect(self.evttrwMovieList_itemselectionchanged)
        self.accepted.connect(self.evt_actorWindow_accepted)

        # fire events once to set btn enablements initially
        self.evttrwMovieList_itemselectionchanged()

        # set the icons for the buttonbox
        self.buttonBox.button(QDialogButtonBox.Ok).setIcon(QIcon(":/icons/film_save.png"))
        self.buttonBox.button(QDialogButtonBox.Ok).setIconSize(QSize(16, 16))
        self.buttonBox.button(QDialogButtonBox.Cancel).setIcon(QIcon(":/icons/cancel.png"))
        self.buttonBox.button(QDialogButtonBox.Cancel).setIconSize(QSize(16, 16))

        self._actorid = actorId

    def evttrwMovieList_itemselectionchanged(self):
        if len(self.trwMovieList.selectedItems()) >= 1:
            self.movieRemove.setEnabled(True)
        else:
            self.movieRemove.setEnabled(False)

    def evtMovieAdd_clicked(self):
        w = SelectionWindow(self, roles.WindowSelectionRoles.MOVIE)
        if w.exec_() == QDialog.Accepted:
            for id in w.getSelectedIds(roles.UserRoles.MOVIE_ID):
                found = False
                for i in range(0, self.trwMovieList.topLevelItemCount()):
                    if self.trwMovieList.topLevelItem(i).data(0, roles.UserRoles.MOVIE_ID.value) == id:
                        found = True
                        break

                if not found:
                    item = QTreeWidgetItem(self.trwMovieList)
                    movie = Movie.getMovieById(id)
                    item.setText(0, movie.title)
                    item.setData(0, roles.UserRoles.MOVIE_ID.value, movie.id)
                    self.trwMovieList.addTopLevelItem(item)

    def evtMovieRemove_clicked(self):
        for item in self.trwMovieList.selectedItems():
            self.trwMovieList.invisibleRootItem().removeChild(item)

    def evt_actorWindow_accepted(self):
        act = Actor(
            id_=self._actorid,
            prename=self.ledPrename.text(),
            name=self.ledName.text(),
        )

        movieIds = list()
        for i in range(0, self.trwMovieList.topLevelItemCount()):
            movieIds.append(int(self.trwMovieList.topLevelItem(i).data(0, roles.UserRoles.MOVIE_ID.value)))
        act.setMovies(movieIds)

        act.save()

    def done(self, result):
        if result == QDialog.Accepted:
            if self.ledName.text() == "":
                QMessageBox.warning(self, "Error", "Please enter a Name", QMessageBox.Ok)
                return
            if self.ledPrename.text() == "":
                QMessageBox.warning(self, "Error", "Please enter a Prename", QMessageBox.Ok)
                return

        super().done(result)