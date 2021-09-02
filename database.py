import glob
import os
import re
import sys
import sqlparse

from PyQt5.QtCore import QMutex
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QMessageBox


class Database:
    _instance: object = None
    _mutex: QMutex = QMutex()
    _db: QSqlDatabase = None

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

                # When a Database Instance is opened we will perform any outstanding
                # schema updates
                Database._perform_migrations(Database._instance)

            Database._mutex.unlock()
        return Database._instance

    def __init__(self):
        pass

    def getQuery(self) -> QSqlQuery:
        return QSqlQuery(self._db)

    def getDatabase(self) -> QSqlDatabase:
        return self._db

    def _perform_migrations(self):
        qry = self.getQuery()
        d = self.getDatabase()

        print("Performing outstanding Database migrations...")

        # first check if we can query a version of
        # the schema_changes table, if not possible
        # we likely need to create a completly new db
        if qry.exec("SELECT version FROM schema_changes ORDER BY version DESC LIMIT 1") and qry.next():
            version = int(qry.value(0))
            print(f"Found Database Version to be {version}")
        else:
            version = -1
            print("Could not determine database version, will create new schema from scratch...")

        files = glob.glob("sql/*.sql")
        if len(files) > 0:
            # when there are files available, we will query all the migrations
            # this way we can tell in the logs when a previous migration was applied
            qry.exec("SELECT version, apply_date FROM schema_changes ORDER BY version ASC")
            all_migrations = dict()
            while qry.next():
                all_migrations[qry.value(0)] = qry.value(1)

            # we will iterate over a sorted set of our sql files
            # the re.findall will only consider the digits in the filename
            # which we will use as our version id
            d.transaction()
            for file in sorted(files, key=lambda x: float(re.findall(r"(\d+)", x)[0])):
                scriptname: str = os.path.basename(file)
                try:
                    file_version = int(scriptname.split("_", 1)[0])
                except ValueError:
                    print(f"{scriptname} is an invalid sql filename.")
                    print("Exiting now ...")
                    sys.exit(1)

                # if the database version is already higher then the version in the filename
                # we may skip this sql file
                if version >= file_version:
                    print(f"Skipping {scriptname}, because migration {file_version} was already applied on {all_migrations.get(file_version, 'NULL')}")
                else:
                    # otherwise we will execute the sql code and apply the migration
                    with open(file, 'rt', encoding='utf-8') as fd:
                        sql = fd.read()
                        # We will have to use sqlparser to split our migration files
                        # into atomic statements since the sqlite qt driver does not
                        # work with multiple stmts in one exec call and offers itself
                        # no alternative like the sqlite3.executescript() that comes
                        # with python3... :(
                        for stmt in sqlparse.split(sql):
                            if not qry.exec(stmt):
                                print(f"Applying {scriptname} to schema failed")
                                print(f"The error appeared with the following statement:")
                                print(stmt)
                                print(qry.lastError().text())
                                d.rollback()
                                sys.exit(1)

                    if not qry.exec(f"""
                            INSERT INTO schema_changes 
                                (version, scriptname, apply_date)
                            VALUES
                                ({file_version}, '{scriptname}', DATETIME('now'))
                            """):
                        print(qry.lastError().text())
                        d.rollback()
                        sys.exit(1)
                    else:
                        print(f"Successfully applied {scriptname} to schema")

            # if we come this far we've applied all outstanding migrations
            # and can commit all changes to disk
            d.commit()
            print(f"All outstanding db migrations were applied")
            print(f"Database schema is now at version: {file_version}")
        else:
            print("Could not find any Schema Files in sql/*.sql - Please reinstall application.")
            print("Exiting now ...")
            sys.exit(1)

    @staticmethod
    def getInstance():
        return Database()
