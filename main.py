import sys
from PyQt5.QtWidgets import QApplication
from windows import mainwindow
import ctypes

from database import Database

if sys.platform.startswith('win32'):
    # make windows show the correct icon even if hosted through pythonw.exe
    myappid = 'de.almdudler777.pydvdorganizer'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

translator = None

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Call DB getInstance once here before the mainwindow is shown
    # this will perform migrations and may crash, but it will prevent
    # the window from flashing (opening and immediatly closing)
    Database.getInstance()

    mainWindow = mainwindow.MainWindow()
    mainWindow.show()
    app.exec_()



"""
    translator = QTranslator()
    # look up e.g. :/i18n/myapp_de.qm
    if translator.load(QLocale(), "myapp"), QLatin1String("_"), QLatin1String(":/i18n"):
        QCoreApplication.installTranslator(translator)
         
    #print(translator.load("qt_pl", QLibraryInfo.location(QLibraryInfo.TranslationsPath)))
    #print(translator.load("de_DEs", "translations"))
    #app.installTranslator(translator)
    
    for w in QApplication.topLevelWidgets():
        if isinstance(w, QDialog) or isinstance(w, QMainWindow):
            pass
"""
