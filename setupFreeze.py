import sys
from cx_Freeze import setup, Executable

# Aggiungi qui eventuali pacchetti che vuoi includere
packages = [
    "numpy",
    "cv2",
    "psutil",
    "PyQt5",
    "PyQt5.Qt",
    "PyQt5.QtCore",
    "PyQt5.QtGui",
    "PyQt5.QtWidgets",
    "PyQt5.QtXml",
]

options = {
    'build_exe': {
        'packages': packages,
        'include_files': [
            r'C:\Users\aless\OneDrive\Desktop\ArchivioPy\biggusPy1.3.1\BiggusMain\elements\imgs\BiggusIcon.ico'
        ]
    }
}

executables = [
    Executable(r'C:\Users\aless\OneDrive\Desktop\ArchivioPy\biggusPy1.3.1\main.py', base=None, icon=r'C:\Users\aless\OneDrive\Desktop\ArchivioPy\biggusPy1.3.1\BiggusMain\elements\imgs\BiggusIcon.ico')
]

setup(name='biggusPy',
      version='1.0',
      description='the great Caesar Friend',
      options=options,
      executables=executables)