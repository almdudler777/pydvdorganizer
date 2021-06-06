from PyQt5.QtCore import QEvent, QTranslator
from PyQt5.QtWidgets import QDialog, QWidget, QApplication, QMainWindow

import main
from ui_modules.configwindow import Ui_configWindow


class ConfigWindow(QDialog, Ui_configWindow):

    def __init__(self, parent: QWidget):
        super(ConfigWindow, self).__init__(parent)
        self.setupUi(self)

        options = [
            ("English", None),
            ("Deutsch", "de_DE"),
        ]

        main.translator = QTranslator(QApplication.instance())

        for i, (text, lang) in enumerate(options):
            self.cbLanguage.addItem(text)
            self.cbLanguage.setItemData(i, lang)
        self.retranslateUi(self)

        # Signal setup
        self.cbLanguage.currentIndexChanged.connect(self.change_language)

    def change_language(self, index):
        data = self.cbLanguage.itemData(index)
        if data:
            main.translator.load(data, "translations")
            QApplication.instance().installTranslator(main.translator)
        else:
            QApplication.instance().removeTranslator(main.translator)

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            self.retranslateUi(self)
        super().changeEvent(event)