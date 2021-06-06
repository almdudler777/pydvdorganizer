import sys

from PyQt5.QtCore import QTranslator
from PyQt5.QtWidgets import QApplication
import mainwindow
import ctypes

# make windows show the correct icon even if hosted through pythonw.exe
myappid = 'almdudler777.de.pydvdorganizer.0815' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

translator = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = mainwindow.MainWindow()
    mainWindow.show()
    app.exec_()


#pyinstaller.exe --onefile --windowed --icon ui\res\50px-Dvd_icon.svg.ico main.py
#pyrcc5 resources.qrc -o resources.py
#pyuic5.exe --import-from=ui_modules -o ui_modules\actorwindow.py ui\actorwindow.ui
#pyrcc5 ui\res\resources.qrc -o ui_modules\resources_rc.py
#env\Scripts\pylupdate5.exe translations\my.pro
#pylupdate4 *.py *.pyw -ts imagechanger_fr.ts
#pylupdate5 main.py  -ts eng-chs.ts
#pylupdate5 main.py  -ts eng-fr.ts
#lrelease eng-fr.ts eng-chs.qm
#env\Scripts\pylupdate5.exe -noobsolete translations\my.pro
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
        
<!DOCTYPE RCC><RCC version="1.0">
<qresource>
    <file>translations/i18n_ar.qm</file>
    <file>translations/i18n_cs.qm</file>
    <file>translations/i18n_de.qm</file>
    <file>translations/i18n_el.qm</file>
    <file>translations/i18n_en.qm</file>
    <file>translations/i18n_eo.qm</file>
    <file>translations/i18n_fr.qm</file>
    <file>translations/i18n_it.qm</file>
    <file>translations/i18n_jp.qm</file>
    <file>translations/i18n_ko.qm</file>
    <file>translations/i18n_no.qm</file>
    <file>translations/i18n_ru.qm</file>
    <file>translations/i18n_sv.qm</file>
    <file>translations/i18n_zh.qm</file>
</qresource>
</RCC>        
"""
