from PyQt5.QtCore import QMutex
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QMessageBox
import sys


class Database():

    _instance : object = None
    _mutex : QMutex = QMutex()
    _db : QSqlDatabase = None

    def __new__(cls):
        if Database._instance is None:
            Database._mutex.lock()

            if Database._instance is None:
                Database._instance = super(Database, cls).__new__(cls)
                Database._db = QSqlDatabase.addDatabase("QSQLITE")
                Database._db.setDatabaseName("data.sqlite")

                if not Database._db.open():
                    QMessageBox.critical(None, "Database Error", Database._db.lastError().text())
                    sys.exit(0)

            Database._mutex.unlock()
        return Database._instance

    def __init__(self):
        pass

    def getQuery(self) -> QSqlQuery:
        return QSqlQuery(self._db)

    def getDatabase(self) -> QSqlDatabase:
        return self._db

    @staticmethod
    def getInstance():
        return Database()