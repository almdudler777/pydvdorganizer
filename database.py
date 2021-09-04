import glob
import os
import re
import sys
import sqlparse

from PyQt5.QtCore import QMutex, QDir, QFile, QTextStream
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QMessageBox

import sql.migrations_rc

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

        # check if we can query a version of
        # the schema_changes table, if not possible
        # we likely need to create a completly new db
        if qry.exec("SELECT version FROM schema_changes ORDER BY version DESC LIMIT 1") and qry.next():
            db_version = int(qry.value(0))
            print(f"Found Database Version to be {db_version}")
        else:
            db_version = -1
            print("Could not determine database version, will create new schema from scratch...")

        # check to see if we can find any migration files
        # we will prefer the ones in sql/*.sql on disk over the ones
        # bundled with qrc for easier development, but the release version
        # will likely use the ones bundled with the applications ressources
        files = glob.glob("sql/*.sql")
        if len(files) == 0:
            # could not find any files on disk in sql subdir
            if QDir(":/sql").exists():
                dir_ = QDir(":/sql")
                dir_.setNameFilters(["*.sql"])
                # in QDir.entryList files will be stripped of path
                # and we also need to append :
                files = [":/sql/" + x for x in dir_.entryList(filters=QDir.Files)]

        # if the number of files is still zero we could not find any migrations
        # this would be a bug and we can terminate
        if len(files) == 0:
            print("Could not find any Schema Files in sql/*.sql - Please reinstall application.")
            print("Exiting now ...")
            sys.exit(1)
        else:
            # next we sort the files in the correct order
            files = sorted(files, key=lambda x: float(re.findall(r"(\d+)", x)[0]))
            # next up, we check the highest migration file version number
            # this should be the last list entry
            # if thats higher than db version we migrate
            # otherwise we return early doing nothing
            highvers = self._get_migrationfile_version(os.path.basename(files[-1]))
            if highvers <= db_version:
                print(f"Found highest Version of migration files is {highvers}")
                print("Nothing needs to be migrated.")
                return

            print("Performing outstanding Database migrations...")
            qry.exec("SELECT version, apply_date FROM schema_changes ORDER BY version ASC")
            all_migrations = dict()
            while qry.next():
                all_migrations[qry.value(0)] = qry.value(1)

            d.transaction()
            for file in files:
                scriptname: str = os.path.basename(file)
                file_version = self._get_migrationfile_version(scriptname)

                # if the database version is already higher then the version in the filename
                # we may skip this sql file
                if db_version >= file_version:
                    print(f"Skipping {scriptname}, because migration {file_version} was already applied on {all_migrations.get(file_version, 'NULL')}")
                else:
                    # otherwise we will execute the sql code and apply the migration
                    try:
                        if file.startswith(":"):
                            fd = QFile(file)
                            fd.open(QFile.ReadOnly | QFile.Text)
                            sql = QTextStream(fd).readAll()
                        else:
                            with open(file, 'rt', encoding='utf-8') as fd:
                                sql = fd.read()
                    except OSError:
                        print(f"Could not open file for reading: {file}")
                        sys.exit(1)
                    finally:
                        if file.startswith(":"):
                            fd.close()

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

    def _get_migrationfile_version(self, scriptname):
        try:
            file_version = int(scriptname.split("_", 1)[0])
        except ValueError:
            print(f"{scriptname} is an invalid sql filename.")
            print("Exiting now ...")
            sys.exit(1)
        return file_version

    @staticmethod
    def getInstance():
        return Database()
