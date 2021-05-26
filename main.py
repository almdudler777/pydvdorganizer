import sys
from PyQt5.QtWidgets import QApplication
import mainwindow
import ctypes

# make windows show the correct icon even if hosted through pythonw.exe
myappid = 'almdudler777.de.pydvdorganizer.0815' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = mainwindow.MainWindow()
    mainWindow.show()
    app.exec_()


#pyinstaller.exe --onefile --windowed --icon ui\res\50px-Dvd_icon.svg.ico main.py
#pyrcc5 resources.qrc -o resources.py
#pyuic5.exe --import-from=ui_modules -o ui_modules\actorwindow.py ui\actorwindow.ui
#pyrcc5 ui\res\resources.qrc -o ui_modules\resources_rc.py