#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import os
import sys

if sys.platform.startswith('win32'):
    binary_pyuic5="pyuic5.exe"
    binary_pylupdate5="pylupdate5.exe"
    binary_qt5tools="qt5-tools.exe"
elif sys.platform.startswith('linux'):
    binary_pyuic5="pyuic5"
    binary_pylupdate5 = "pylupdate5"
    binary_qt5tools = "qt5-tools"
else:
    print("OS Type not supported.")
    exit(1)

# recompile the ui files to ui_modules
# this should be safe, as long as we subclass our window.py-files
print("Compiling ui-files using pyuic5...")
for uifile in Path('ui/').rglob('*.ui'):
    filename = uifile.name.replace('.ui','')
    cmd = f"{binary_pyuic5} --import-from=ui_modules -o ui_modules/{filename}.py ui/{filename}.ui"
    print(f"CMD: {cmd}")
    os.system(cmd)

# update translations
tr_sources = [
    'main.py',
    'mainwindow.py',
    'ui_modules/mainwindow.py',
    'configwindow.py',
    'ui_modules/configwindow.py',
    'moviewindow.py',
    'ui_modules/moviewindow.py',
]

ts_files = [
    'de_DE',
    'fr_FR'
]

print("")
print("Creating translation base-files...")
for ts_file in ts_files:
    cmd = f"{binary_pylupdate5} -verbose -noobsolete {' '.join(tr_sources)} -ts translations/{ts_file}.ts"
    print(f"CMD: {cmd}")
    os.system(cmd)
    cmd = f"{binary_qt5tools} lrelease -compress translations/{ts_file}.ts"
    print(f"CMD: {cmd}")
    os.system(cmd)


print("")
print("Creating translation ressource file...")
files = ""
for qmfile in Path('translations/').rglob('*.qm'):
    files += "<file>{}</file>".format(qmfile.name)

with open("translations/translations.qrc", "wt") as qrcfile:
    qrcfile.write("""<!DOCTYPE RCC><RCC version="1.0">
<qresource prefix="translations">
    {}
</qresource>
</RCC>   
    """.format(files))

print("Written translations.qrc ... Compiling ...")
cmd = f"pyrcc5 translations/translations.qrc -o translations/translations_rc.py"
print(cmd)
os.system(cmd)



#pyinstaller.exe --onefile --windowed --icon ui\res\logo.ico main.py
#env\Scripts\pylupdate5.exe translations\my.pro
#pylupdate5 main.py  -ts eng-fr.ts
#lrelease eng-fr.ts eng-chs.qm
#env\Scripts\pylupdate5.exe -noobsolete translations\my.pro