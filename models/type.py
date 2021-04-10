from database import Database as db


class Type:

    def __init__(self, id: int, name: str):
        self._id = id
        self.name = name

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id_):
        pass

    def __str__(self):
        return "Type: {} (ID:{})".format(self.name, self.id)

    def getMovieCount(self):
        ret = 0
        qry = db.getInstance().getQuery()
        if qry.exec("SELECT count(*) FROM movies WHERE type_id = {}".format(self.id)) and qry.next():
            ret = int(qry.value(0))
        qry.clear()
        return ret

    def getMovies(self):
        from .movie import Movie
        return Movie.getMoviesByType(self)

    @classmethod
    def getTypeById(cls, typeid: int):
        ret = None
        qry = db.getInstance().getQuery()
        if qry.exec("SELECT id, name FROM type WHERE id = {}".format(typeid)) and qry.next():
            ret = Type(id=int(qry.value(0)), name=str(qry.value(1)))
        qry.clear()
        return ret

    @classmethod
    def getTypeCount(cls):
        ret = 0
        qry = db.getInstance().getQuery()
        if qry.exec("SELECT count(*) FROM type") and qry.next():
            ret = int(qry.value(0))
        qry.clear()
        return ret

    @classmethod
    def getAllTypes(cls):
        qry = db.getInstance().getQuery()
        ret: list = list()
        if qry.exec("SELECT id, name FROM type"):
            while qry.next():
                ret.append(
                    Type(
                        id=int(qry.value(0)),
                        name=str(qry.value(1))
                    )
                )
        qry.clear()
        return ret
