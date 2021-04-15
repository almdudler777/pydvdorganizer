from PyQt5.QtCore import Qt, QSize, QDate, QVariant
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTreeWidgetItem, QDialogButtonBox, QDialog, QWidget, QMessageBox

import roles
from models import Movie, Type, Actor, Category
from selectionwindow import SelectionWindow
from ui_modules.actorwindow import Ui_actorWindow


class ActorWindow(QDialog, Ui_actorWindow):

    def __init__(self, parent: QWidget, movieId: int = 0):
        super(ActorWindow, self).__init__(parent)
        self.setupUi(self)

        # connect signals
        self.movieAdd.clicked.connect(self.evtMovieAdd_clicked)
        self.movieRemove.clicked.connect(self.evtMovieRemove_clicked)

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
