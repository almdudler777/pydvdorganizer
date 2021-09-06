from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QHeaderView, QMainWindow, QMessageBox, QTreeWidgetItem, QDialog

import roles
from .actorwindow import ActorWindow
from .configwindow import ConfigWindow
from .moviewindow import MovieWindow
from models import Movie

from ui_modules.mainwindow import Ui_MainWindow
import math


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.showMaximized()

        # set up the main treewidget stretching
        header = self.trwMovieList.header()
        header.setMinimumSectionSize(50)
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.Stretch)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        header.setStretchLastSection(False)

        self.currentPage = 0
        self.handlePages()

        self.populateMovieListWidget()
        self.trwMovieList.sortByColumn(0, Qt.AscendingOrder)

        # Signal setup
        self.actionAbout_Qt.triggered.connect(self.evtAboutQtTriggered)
        self.actionAbout.triggered.connect(self.evtAboutTriggered)
        self.actionClose.triggered.connect(self.close)
        self.actionNewMovie.triggered.connect(self.evtActionNewMovie_triggered)
        self.actionNewActor.triggered.connect(self.evtactionNeuer_Schauspieler_triggered)
        self.trwMovieList.itemDoubleClicked.connect(self.evtMovieList_itemDoubleClicked)
        self.cbxPerPage.activated.connect(self.evtcbxPerPage_activated)
        self.btnPageBack.clicked.connect(self.evtbtnPageBack_clicked)
        self.btnPageForth.clicked.connect(self.evtbtnPageForth_clicked)
        self.cbxPageSelector.activated.connect(self.evtcbxPageSelector_activated)
        self.actionProperties.triggered.connect(self.evtPropertiesTriggered)

    def evtPropertiesTriggered(self):
        w = ConfigWindow(self)
        if w.exec_() == QDialog.Accepted:
            pass # TODO: complete

    def evtAboutQtTriggered(self):
        QMessageBox.aboutQt(self)

    def evtAboutTriggered(self):
        QMessageBox.about(self, "PyDVDOrganizer", "by almdudler777.de")

    def evtActionNewMovie_triggered(self):
        w = MovieWindow(self)
        if w.exec_() == QDialog.Accepted:
            self.populateMovieListWidget()

    def evtactionNeuer_Schauspieler_triggered(self):
        w = ActorWindow(self)
        if w.exec_() == QDialog.Accepted:
            self.populateMovieListWidget()

    def evtMovieList_itemDoubleClicked(self, item: QTreeWidgetItem, column: int):
        w = MovieWindow(self, int(item.data(0, roles.UserRoles.MOVIE_ID.value)))
        if w.exec_() == QDialog.Accepted:
            self.populateMovieListWidget()

    def evtcbxPerPage_activated(self, arg: int):
        self.handlePages()

    def evtbtnPageForth_clicked(self):
        self.currentPage += 1
        self.handlePages()

    def evtbtnPageBack_clicked(self):
        if self.currentPage > 0:
            self.currentPage -= 1
        self.handlePages()

    def evtcbxPageSelector_activated(self, index: int):
        self.currentPage = index
        self.handlePages()

    def populateDatabaseFilterWidget(self):
        pass

    def populateMovieListWidget(self):
        allMovies = Movie.getAllMovies(self.currentPage * self.getPerPage(), self.getPerPage())
        self.trwMovieList.clear()

        for movie in allMovies:
            item = QTreeWidgetItem(self.trwMovieList)
            item.setText(0, movie.title)
            item.setText(1, str(movie.length))
            item.setText(2, str(movie.mediums))
            item.setText(3, str(movie.rated))
            item.setText(4, movie.getCategoriesAsCommaSeparatedString())
            item.setText(5, movie.getActorsAsCommaSeparatedString())
            item.setText(6, "%.2f €" % movie.cost)
            item.setData(0, roles.UserRoles.MOVIE_ID.value, movie.id)
            self.trwMovieList.addTopLevelItem(item)

            for i in range(0, self.trwMovieList.columnCount()):
                item.setTextAlignment(i, self.trwMovieList.headerItem().textAlignment(i))

            item.setTextAlignment(item.columnCount() - 1, Qt.AlignRight)

        allMovies.clear()

    def handlePages(self):
        numberOfPages = 0
        if self.getPerPage() != -1:
            numberOfPages = math.trunc(Movie.getMovieCount() / self.getPerPage())
            if self.currentPage > numberOfPages:
                self.currentPage = numberOfPages

            # disable back button if we're on first page
            self.btnPageBack.setEnabled(False if self.currentPage == 0 else True)
            # disable forward button if were on the last page
            self.btnPageForth.setEnabled(False if self.currentPage == numberOfPages else True)
            self.cbxPageSelector.setEnabled(True)
        else:
            self.btnPageForth.setEnabled(False)
            self.btnPageBack.setEnabled(False)
            self.cbxPageSelector.setEnabled(False)

        self.cbxPageSelector.clear()
        for i in range(1, numberOfPages + 2):
            self.cbxPageSelector.addItem(str(i))
        self.cbxPageSelector.setCurrentIndex(self.currentPage)
        self.populateMovieListWidget()

    def getPerPage(self):
        if self.cbxPerPage.currentIndex() > 0:
            return int(self.cbxPerPage.currentText())
        else:
            '''
            if paging should be disabled we will return -1
            this will result in sqlite eventually filtering for
            SELECT ... LIMIT (currentPage * -1), (getPerPage => -1)
            => LIMIT -1, -1 which will be graciously ignored by sqlite
            '''
            return -1

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            self.retranslateUi(self)
        super().changeEvent(event)