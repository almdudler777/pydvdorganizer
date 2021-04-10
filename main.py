import sys
from PyQt5.QtWidgets import QApplication
import mainwindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = mainwindow.MainWindow()
    mainWindow.show()
    app.exec_()
