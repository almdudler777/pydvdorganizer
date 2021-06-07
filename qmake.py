#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import os

# recompile the ui files to ui_modules
# this should be safe, as long as we subclass our window.py-files
print("Compiling ui-files using pyuic5.exe...")
for uifile in Path('ui/').rglob('*.ui'):
    filename = uifile.name.replace('.ui','')
    cmd = f"pyuic5.exe --import-from=ui_modules -o ui_modules/{filename}.py ui/{filename}.ui"
    print(f"CMD: {cmd}")
    os.system(cmd)

# update translations
tr_sources = [
    'main.py',
    'mainwindow.py',
    'ui_modules/mainwindow.py',
    'configwindow.py',
    'ui_modules/configwindow.py',
]

ts_files = [
    'de_DE'
]

print("")
print("Creating translation base-files...")
for ts_file in ts_files:
    cmd = f"pylupdate5.exe -verbose -noobsolete {' '.join(tr_sources)} -ts translations/{ts_file}.ts"
    os.system(cmd)

#pyinstaller.exe --onefile --windowed --icon ui\res\logo.ico main.py
#pyrcc5 resources.qrc -o resources.py
#pyuic5.exe --import-from=ui_modules -o ui_modules\actorwindow.py ui\actorwindow.ui
#pyrcc5 ui\res\resources.qrc -o ui_modules\resources_rc.py
#env\Scripts\pylupdate5.exe translations\my.pro
#pylupdate5 main.py  -ts eng-fr.ts
#lrelease eng-fr.ts eng-chs.qm
#env\Scripts\pylupdate5.exe -noobsolete translations\my.pro