from PyQt5.QtWidgets import QMessageBox

from database import Database as db


class Category:

    def __init__(self, id_: int, name: str):
        self._id = id_
        self.name = name

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id_):
        pass

    def __str__(self):
        return "{} (ID:{})".format(self.name, self.id)

    def getMovieCount(self):
        ret: int = 0
        qry = db.getInstance().getQuery()
        qry.prepare("SELECT count(*) FROM tags WHERE category_id = ?")
        qry.addBindValue(self.id)
        if qry.exec() and qry.next():
            ret = int(qry.value(0))
        qry.clear()
        return ret

    @classmethod
    def getCategoryById(cls, id_: int):
        ret: Category = None
        qry = db.getInstance().getQuery()
        qry.prepare("SELECT id,name FROM category WHERE id = ?")
        qry.addBindValue(id_)
        if qry.exec() and qry.next():
            ret = Category(
                id_=int(qry.value(0)),
                name=str(qry.value(1))
            )
        qry.clear()
        return ret

    @classmethod
    def getAllCategories(cls):
        ret: list = list()
        qry = db.getInstance().getQuery()
        if qry.exec("SELECT id, name FROM category ORDER BY name ASC"):
            while qry.next():
                ret.append(
                    Category(
                        id_=int(qry.value(0)),
                        name=str(qry.value(1))
                    )
                )
        qry.clear()
        return ret

    @classmethod
    def getCategoryCount(cls):
        ret: int = 0
        qry = db.getInstance().getQuery()
        if qry.exec("SELECT count(*) FROM category") and qry.next():
            ret = int(qry.value(0))
        qry.clear()
        return ret

    @classmethod
    def getCategoriesByMovieId(cls, movieId: int):
        ret: list = list()
        qry = db.getInstance().getQuery()
        qry.prepare("SELECT id, name FROM category WHERE id IN (SELECT category_id FROM tags WHERE movie_id = ?)")
        qry.addBindValue(movieId)
        if qry.exec():
            while qry.next():
                ret.append(
                    Category(
                        id_=int(qry.value(0)),
                        name=str(qry.value(1))
                    )
                )
        else:
            QMessageBox.warning(None, "Error in getCategoriesByMovieId", qry.lastError().text(), QMessageBox.Ok)
        qry.clear()
        return ret
