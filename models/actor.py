from PyQt5.QtWidgets import QMessageBox
from database import Database as db


class Actor:

    def __init__(self, name: str, prename: str, id_: int):
        self._id = id_
        self.name = name
        self.prename = prename
        self._myMovieIds = list()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id_):
        pass

    def __str__(self):
        return "{}, {} (ID:{})".format(self.name, self.prename, self.id)

    def getMovieCount(self) -> int:
        qry = db.getInstance().getQuery()
        ret: int = 0
        qry.prepare("SELECT count(*) FROM cast WHERE actor_id = ?")
        qry.addBindValue(self.id)
        if qry.exec() and qry.next():
            ret = int(qry.value(0))
        qry.clear()
        return ret

    def setMovies(self, movieIds: list):
        self._myMovieIds.clear()
        self._myMovieIds.extend(movieIds)

    def getMovies(self):
        from models import Movie
        return Movie.getMoviesByActor(self)

    def save(self):
        qry = db.getInstance().getQuery()
        d = db.getInstance().getDatabase()
        d.transaction()

        if self._id == 0:
            if qry.exec("INSERT INTO actors (`name`) VALUES ('New Item')"):
                self._id = int(qry.lastInsertId())
                qry.clear()
            else:
                QMessageBox.warning(None, "Could not create new Actor.", qry.lastError().text(), QMessageBox.Ok)
                d.rollback()
                return

        qry.prepare("UPDATE actors "
                    "SET prename = ?, name = ? "
                    "WHERE id = ?")
        qry.addBindValue(self.prename)
        qry.addBindValue(self.name)
        qry.addBindValue(self._id)

        if not qry.exec():
            QMessageBox.critical(None, "Error while saving.", qry.lastError().text() + qry.executedQuery(), QMessageBox.Ok)
            d.rollback()
            return

        if isinstance(self._myMovieIds, list) and len(self._myMovieIds) > 0:
            qry.exec("DELETE FROM cast WHERE actor_id = {}".format(self._id))
            qry.clear()

            qry.prepare("INSERT INTO cast (movie_id, actor_id) VALUES (?,?)")
            for id in self._myMovieIds:
                qry.addBindValue(id)
                qry.addBindValue(self._id)
                qry.exec()

        d.commit()
        qry.clear()

    @classmethod
    def getAllActors(cls) -> list:
        ret: list = list()
        qry = db.getInstance().getQuery()
        qry.setForwardOnly(True)

        if qry.exec("SELECT name, prename, id FROM actors ORDER BY name ASC"):
            while qry.next():
                ret.append(
                    Actor(
                        str(qry.value(0)),
                        str(qry.value(1)),
                        int(qry.value(2))
                    )
                )
        qry.clear()
        return ret

    @classmethod
    def getActorsByMovieId(cls, movieId: int) -> list:
        ret: list = list()
        qry = db.getInstance().getQuery()
        qry.setForwardOnly(True)

        qry.prepare("SELECT name, prename, id FROM actors WHERE id IN (SELECT actor_id FROM cast WHERE movie_id = ?)")
        qry.addBindValue(movieId)

        if qry.exec():
            while qry.next():
                ret.append(
                    Actor(
                        str(qry.value(0)),
                        str(qry.value(1)),
                        int(qry.value(2))
                    )
                )
        else:
            QMessageBox.warning(None, "Error in getActorsByMovieId", qry.lastError().text(), QMessageBox.Ok)

        qry.clear()
        return ret

    @classmethod
    def getActorCount(cls) -> int:
        ret: int = -1
        qry = db.getInstance().getQuery()

        if qry.exec("SELECT count(*) FROM actors") and qry.next():
            ret = int(qry.value(0))

        qry.clear()
        return ret

    @classmethod
    def getActorById(cls, id_: int):
        ret: Actor = None
        qry = db.getInstance().getQuery()

        if qry.exec("SELECT id, name, prename FROM actors WHERE id = {}".format(id_)) and qry.next():
            ret = Actor(
                str(qry.value(1)),
                str(qry.value(2)),
                int(qry.value(0))
            )
        qry.clear()
        return ret
