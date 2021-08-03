from __future__ import annotations
from PyQt5.QtWidgets import QMessageBox
from typing import List

from database import Database as db
from .actor import Actor
from .category import Category
from .type import Type


class Movie:

    def __init__(self,
                 id: int,
                 title: str,
                 length: int,
                 mediums: int,
                 rated: int,
                 cost: float,
                 type: Type = None):
        self._id = id
        self.title = title
        self.length = length
        self.mediums = mediums
        self.rated = rated
        self.cost = cost
        self.myActorIds = list()
        self.myCategoryIds = list()
        self._type = type

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id_):
        pass

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type: Type):
        self._type = type

    def __str__(self):
        return "{} (ID:{})".format(self.title, self.id)

    def setActors(self, actorIds: list):
        self.myActorIds.clear()
        self.myActorIds.extend(actorIds)

    def setCategories(self, categoryIds):
        self.myCategoryIds.clear()
        self.myCategoryIds.extend(categoryIds)

    def getActors(self) -> list:
        return Actor.getActorsByMovieId(self.id)

    def getActorsAsCommaSeparatedString(self) -> str:
        tmp = self.getActors()
        ret = list()
        for actor in tmp:
            ret.append("{} {}".format(actor.prename, actor.name))
        return ", ".join(ret)

    def getCategories(self):
        return Category.getCategoriesByMovieId(self.id)

    def getCategoriesAsCommaSeparatedString(self) -> str:
        tmp = self.getCategories()
        ret = list()
        for cat in tmp:
            ret.append("{}".format(cat.name))
        return ", ".join(ret)

    def save(self):
        qry = db.getInstance().getQuery()
        d = db.getInstance().getDatabase()
        d.transaction()

        # check that type has been set
        # @ TODO may open a selection box in modal dialog to ask for type?
        if not isinstance(self._type, Type):
            QMessageBox.warning(None, "Type is undefined", "You can not save a movie without a disk type.",
                                QMessageBox.Ok)
            d.rollback()
            return

        # if the movie id is 0 we need to create a new row and later update it
        if self.id == 0:
            if qry.exec("INSERT INTO movies (`title`) VALUES ('New Item')"):
                self._id = int(qry.lastInsertId())
                qry.clear()
            else:
                QMessageBox.warning(None, "Could not create new movie.", qry.lastError().text(), QMessageBox.Ok)
                d.rollback()
                return

        qry.prepare("""
            UPDATE movies 
            SET 
                title = ?, 
                length = ?, 
                discs = ?, 
                rating = ?, 
                price = ?, 
                type_id = ? 
            WHERE id = ?
            """)
        qry.addBindValue(self.title)
        qry.addBindValue(self.length)
        qry.addBindValue(self.mediums)
        qry.addBindValue(self.rated)
        qry.addBindValue(self.cost)
        qry.addBindValue(self.type.id)
        qry.addBindValue(self._id)

        if not qry.exec():
            QMessageBox.critical(None, "Error while saving.", qry.lastError().text(), QMessageBox.Ok)
            d.rollback()
            return

        if isinstance(self.myActorIds, list):
            qry.exec("DELETE FROM cast WHERE movie_id = {}".format(self._id))
            qry.clear()

            qry.prepare("INSERT INTO cast (movie_id, actor_id) VALUES (?,?)")
            for id in self.myActorIds:
                qry.addBindValue(self._id)
                qry.addBindValue(id)
                qry.exec()

        if isinstance(self.myCategoryIds, list):
            qry.exec("DELETE FROM tags WHERE movie_id = {}".format(self._id))
            qry.clear()

            qry.prepare("INSERT INTO tags (movie_id, category_id) VALUES (?,?)")
            for id in self.myCategoryIds:
                qry.addBindValue(self._id)
                qry.addBindValue(id)
                qry.exec()

        d.commit()
        qry.clear()

    @classmethod
    def getAllMovies(cls, start: int = -1, max: int = -1):
        ret: list = list()
        qry = db.getInstance().getQuery()
        qry.setForwardOnly(True)

        if start and start < 0:
            qry.prepare("SELECT id, title, length, discs, rating, price FROM movies ORDER BY title COLLATE NOCASE ASC")
        else:
            qry.prepare(
                "SELECT id, title, length, discs, rating, price FROM movies ORDER BY title COLLATE NOCASE ASC LIMIT ?,?")
            qry.addBindValue(start)
            qry.addBindValue(max)

        if qry.exec():
            while qry.next():
                ret.append(
                    Movie(
                        id=int(qry.value(0)),
                        title=str(qry.value(1)),
                        length=int(qry.value(2)),
                        mediums=int(qry.value(3)),
                        rated=int(qry.value(4)),
                        cost=float(qry.value(5))
                    )
                )
        else:
            QMessageBox.warning(None, "Error in getAllMovies", qry.lastError().text(), QMessageBox.Ok)

        qry.clear()
        return ret

    @classmethod
    def getMovieCount(cls):
        ret: int = 0
        qry = db.getInstance().getQuery()
        if qry.exec("SELECT count(*) FROM movies") and qry.next():
            ret = int(qry.value(0))
        qry.clear()
        return ret

    @classmethod
    def getMovieById(cls, id_: int):
        ret: Movie = None
        qry = db.getInstance().getQuery()
        qry.prepare("SELECT id, title, length, discs, rating, price, type_id FROM movies WHERE id = ?")
        qry.addBindValue(id_)
        if qry.exec() and qry.next():
            ret = Movie(
                id=int(qry.value(0)),
                title=str(qry.value(1)),
                length=int(qry.value(2)),
                mediums=int(qry.value(3)),
                rated=int(qry.value(4)),
                cost=float(qry.value(5)),
                type=Type.getTypeById(int(qry.value(6)))
            )
        qry.clear()
        return ret

    @classmethod
    def getMoviesByActor(cls, actor: Actor) -> List[Movie]:
        ret: List[Movie] = list()
        qry = db.getInstance().getQuery()
        qry.setForwardOnly(True)
        qry.prepare("SELECT "
                    "id, title, length, discs, rating, price, type_id "
                    "FROM movies "
                    "WHERE id IN ("
                    "SELECT movie_id FROM cast WHERE actor_id = ?"
                    ") "
                    "ORDER BY title "
                    "COLLATE NOCASE ASC")
        qry.addBindValue(actor.id)
        if qry.exec():
            while qry.next():
                ret.append(Movie(
                    id=int(qry.value(0)),
                    title=str(qry.value(1)),
                    length=int(qry.value(2)),
                    mediums=int(qry.value(3)),
                    rated=int(qry.value(4)),
                    cost=float(qry.value(5)),
                    type=Type.getTypeById(int(qry.value(6)))
                ))
        qry.clear()
        return ret

    @classmethod
    def getMoviesByType(cls, type: Type):
        qry = db.getInstance().getQuery()
        qry.setForwardOnly(True)
        ret = list()

        qry.prepare("SELECT id, title, length, discs, rating, price "
                    "FROM movies "
                    "WHERE type_id = ? "
                    "ORDER BY title "
                    "COLLATE NOCASE ASC")
        qry.addBindValue(type.id)
        if qry.exec():
            while qry.next():
                ret.append(
                    Movie(
                        id=int(qry.value(0)),
                        title=str(qry.value(1)),
                        length=int(qry.value(2)),
                        mediums=int(qry.value(3)),
                        rated=int(qry.value(4)),
                        cost=float(qry.value(5)),
                        type=type
                    )
                )
        qry.clear()
        return ret
