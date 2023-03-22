import json
import os
import shutil
import sys
from os.path import exists

from PyQt5.QtGui import QColor, QFont, qRgba
from PyQt5.QtWidgets import QFileDialog

from BiggusMain.biggusPy import BiggusPy

"""
ITA:
    Questa classe risolve alcuni problemi di compatibilità tra sistemi operativi.
    Su linux ad esempio il percorso delle cartelle è: /home/utente/cartella
    Su windows invece il percorso delle cartelle è: C:\\Users\\utente\\cartella
    su mac invece è                                   /Users/utente/cartella
    
    Un altro problema si ha se il programma è compilato con pyInstaller. Cambiano
    alcuni percorsi. in fase di debug il percorso è Release/BiggusMain compilato con pyInstaller
    il percorso è BiggusMain. Inoltre pyInstaller una volta compilato il programma, lo fa funzionare in una 
    cartella temporanea chiamate _IMEIxxxx con un nome che cambia tutte le volte. Non tutti i file vengono
    copiati come ad esempio la cartella biggusForlder che deve essere copiata dentro _IMEIxxxx.
ENG:
    This class solves some compatibility problems between operating systems.
    On linux for example the folder path is: / home / user / folder
    On windows instead the folder path is: C: \ Users \ user \ folder
    on mac instead it is:                     / Users / user / folder
    
    Another problem arises if the program is compiled with pyInstaller. Some paths change.
    in debug mode the path is Release / BiggusMain compiled with pyInstaller
    the path is BiggusMain. In addition, pyInstaller once the program is compiled, it makes it run in a
    temporary folder called _IMEIxxxx with a name that changes every time. Not all files are copied
    as for example the biggusForlder folder which must be copied inside _IMEIxxxx.
    
"""


class ntVsPosixVsFreeze:
    # operative system name
    # 'nt' for windows
    # 'posix' for linux
    # 'mac' for mac
    # 'os2' for os2
    # 'ce' for windows ce
    # 'java' for java
    # 'riscos' for riscos

    os = None
    # if program is compiled or froozen
    isFrozen = False
    configFilePath = "config.json"
    configuration = {}

    def __init__(self):
        self.os = os.name  # 'nt' or 'posix'
        self.biggusPy = BiggusPy()
        print(f"os found: windows {os.name}")
        if self.os == 'nt':
            self.initForNt()
        elif self.os == 'posix':
            self.initForPosix()
        elif self.os == 'mac':
            self.initForMac()
        elif self.os == 'os2':
            self.initForOs2()
        elif self.os == 'ce':
            self.initForCE()
        elif self.os == 'java':
            self.initForJAva()
        elif self.os == 'riscos':
            self.initForRiscOs()

    def initForNt(self):
        if getattr(sys, "frozen", False):
            self.isFrozen = True
            print("Software compiled...")
        else:
            self.isFrozen = False
            print("Software not compiled...")
        self.openConfigFile()

    def initForPosix(self):
        if getattr(sys, "frozen", False):
            print("Software compiled...")
            self.isFrozen = True
        else:
            print("Software not compiled...")
            self.isFrozen = False

    def initForMac(self):
        print(" WARNING: we are currently working on the mac version of the software.\n"
              "Actually full compatibility may not be guaranteed.\n let us know if you have any problems.")
        if getattr(sys, "frozen", False):
            print("Software compiled...")
            self.isFrozen = True
        else:
            print("Software not compiled...")
            self.isFrozen = False

    def initForOs2(self):
        print(" WARNING: we are currently working on the os2 version of the software.\n"
              "Actually full compatibility may not be guaranteed.\n let us know if you have any problems.")
        if getattr(sys, "frozen", False):
            print("Software compiled...")
            self.isFrozen = True
        else:
            print("Software not compiled...")
            self.isFrozen = False

    def initForCE(self):
        print(" WARNING: we are currently working on the windows ce version of the software.\n"
              "Actually full compatibility may not be guaranteed.\n let us know if you have any problems.")
        if getattr(sys, "frozen", False):
            print("Software compiled...")
            self.isFrozen = True
        else:
            print("Software not compiled...")
            self.isFrozen = False

    def initForJAva(self):
        print(" WARNING: we are currently working on the java version of the software.\n"
              "Actually full compatibility may not be guaranteed.\n let us know if you have any problems.")
        if getattr(sys, "frozen", False):
            print("Software compiled...")
            self.isFrozen = True
        else:
            print("Software not compiled...")
            self.isFrozen = False

    def initForRiscOs(self):
        print(" WARNING: we are currently working on the riscos version of the software.\n"
              "Actually full compatibility may not be guaranteed.\n let us know if you have any problems.")
        if getattr(sys, "frozen", False):
            print("Software compiled...")
            self.isFrozen = True
        else:
            print("Software not compiled...")
            self.isFrozen = False

    def openConfigFile(self):
        """
        ITA:
            Apre il file di configurazione. Nel file di configurazione sono salvate le informazioni
            sui percorsi delle cartelle e dei file.
        ENG:
            Open the configuration file. The configuration file stores information
            on the paths of the folders and files.
        :param path:
        :return:
        """
        try:
            with open(self.configFilePath, 'r') as f:
                data = json.load(f)
            self.parseData(data)
            print(f"configuration file Found in {self.configFilePath}")

        except FileNotFoundError:
            print(f"configuration file not found in {self.configFilePath}")
            print("please select the configuration file")
            # If file not found, search for it in the folder where the program is located
            openFileDialog = QFileDialog()
            openFileDialog.setFileMode(QFileDialog.AnyFile)
            openFileDialog.setNameFilter("Json (*.json)")
            openFileDialog.setViewMode(QFileDialog.Detail)
            if self.isFrozen:
                openFileDialog.setDirectory(os.path.dirname(os.path.abspath(sys.executable)))
            else:
                # apre la cartella corrente non quella del main!
                openFileDialog.setDirectory(os.path.dirname(os.path.abspath(__file__)))
            if openFileDialog.exec_():
                configFile = openFileDialog.selectedFiles()[0]
                with open(configFile, "r") as f:
                    data = json.load(f)
                print(f"configuration file Found in {configFile}")
                self.configFilePath = configFile
            else:
                print("No file selected")
                sys.exit(0)

    def parseData(self, data):
        """
        ITA:
            Analizza i dati del file di configurazione.
        ENG:
            Analyze the data of the configuration file.
        :param data:
        :return:
        """
        mainDir = data["mainDir"]
        saveDir = data["saveFileDirectory"]
        iconPath = data["iconPaths"]
        logoPath = data["logoPaths"]
        nodeAndFolderPath = data["nodesFolderPath"]
        if self.isFrozen:
            self.biggusPy.mainDir = os.path.abspath(os.path.join(os.path.dirname(sys.executable), "biggusFolder"))
            self.biggusPy.saveFileDirectory = os.path.abspath(os.path.join(os.path.dirname(sys.executable), saveDir))
            # le icone si trovano in imgs/icons
            for key, value in iconPath.items():
                self.biggusPy.iconPaths[key] = value
            # il logo si trova in imgs/logos
            for key, value in logoPath.items():
                self.biggusPy.logoPaths[key] = value
            # i nodi si trovano in nodes
            for key, value in nodeAndFolderPath.items():
                self.biggusPy.nodesFolderPath[key] = value
        else:
            self.biggusPy.mainDir = os.path.abspath(os.path.join(os.path.dirname(__file__), mainDir))
            self.biggusPy.saveFileDirectory = os.path.abspath(os.path.join(os.path.dirname(__file__), saveDir))
            # le icone si trovano in imgs/icons
            for key, value in iconPath.items():
                self.biggusPy.iconPaths[key] = value
            # il logo si trova in imgs/logos
            for key, value in logoPath.items():
                self.biggusPy.logoPaths[key] = value
            # i nodi si trovano in nodes
            for key, value in nodeAndFolderPath.items():
                self.biggusPy.nodesFolderPath[key] = value
        self.biggusPy.defaultNode = data["defaultNode"]
        # carica il font di sistema e i colori
        self.loadFontAndColor(data)

    def loadFontAndColor(self, data):
        """
        ITA:
            Carica il font di sistema e i colori.
        ENG:
            Load the system font and colors.
        "fontAndColor": {
                        "systemFont": "Noto Serif,16,-1,5,50,0,0,0,0,0",
                        "widgetFont": "Noto Serif,14,-1,5,50,0,0,0,0,0",
                        "widgetOnWidgetFont": "Noto Serif,10,-1,5,50,0,0,0,0,0",
                        "systemFontColor": "(250, 250, 250, 255)",
                        "widgetFontColor": "(250, 250, 250, 255)",
                        "widgetOnWidgetFontColor": "(150, 150, 240, 255)",
                        "systemHighlightColor": "(60, 60, 65, 255)",
                        "systemHighlightTextColor": "(250, 250, 255, 255)",
                        "systemBorderColor": "(40, 40, 45, 255)",
                        "systemBackgroundColor": "(50, 50, 53, 255)",
                        "widgetBorderColor": "(40, 40, 45, 255)",
                        "widgetBackgroundColor": "(39, 39, 40, 255)",
                        "widgetOnWidgetBorderColor": "(40, 40, 45, 255)",
                        "widgetOnWidgetBackgroundColor": "(43, 43, 45, 255)"
                        }
        :param data:
        :return:
        """
        configFontAndColors = data["fontAndColor"]
        for key, value in configFontAndColors.items():
            # se è un font è tipo "font": "MS Shell Dlg 2,8,-1,5,50,0,0,0,0,0",
            # se è un colore è tipo: "systemFontColor": "(250, 250, 250, 255)",
            if "Color" in key:
                # se è un colore
                value = value.replace("(", "")
                value = value.replace(")", "")
                value = value.split(",")
                rgba = qRgba(int(value[0]), int(value[1]), int(value[2]), int(value[3]))
                self.biggusPy.configFontAndColors[key] = QColor(rgba)
            else:
                # se è un font ricava il font e la dimensione dalla stringa "Noto Serif,16,-1,5,50,0,0,0,0,0", e crea un oggetto QFont
                value = value.split(",")
                font = QFont()
                font.setFamily(value[0])
                font.setPointSize(int(value[1]))
                font.fromString(
                    value[0] + "," + value[1] + "," + value[2] + "," + value[3] + "," + value[4] + "," + value[
                        5] + "," + value[6] + "," + value[7] + "," + value[8] + "," + value[9])
                self.biggusPy.configFontAndColors[key] = font

        self.start()

    def start(self):
        """
        ITA:
            Avvia il programma.
        ENG:
            Start the program.
        :return:
        """
        self.biggusPy.start()
        if self.isFrozen:
            if getattr(sys, 'frozen', False):
                # Se siamo in un eseguibile PyInstaller, cambiamo il percorso di ricerca dei moduli
                # per far sì che punti alla cartella temporanea creata da PyInstaller
                nodes_folder = sys._MEIPASS
                print(f"nodes_folder: {nodes_folder} compiled version")
                moduleFolder = os.path.join(nodes_folder, "biggusFolder")
                print(f"folder to copy: {moduleFolder}")
                if not exists(moduleFolder):
                    print("folder not exists")
                    srcDir = os.path.join(os.getcwd(), "biggusFolder")
                    destDir = os.path.join(nodes_folder, "biggusFolder")
                    shutil.copytree(srcDir, moduleFolder)
                    if not exists(destDir):
                        print("ERROR: moduleFolder not found")
                        raise Exception("ERROR: moduleFolder not found")
        self.biggusPy.show()