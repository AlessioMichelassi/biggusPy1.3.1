def setMainDirectoryMacLinux(self, _directory):
    self.mainDir = _directory
    self.nodesFolderPath = {}
    for folder in os.listdir(f"{self.mainDir}/Nodes"):
        if not os.path.isfile(f"{self.mainDir}/Nodes/{folder}"):
            # example: "python"
            key = folder
            # example: "Release/biggusFolder/Nodes/PythonNodes"
            value = f"{self.mainDir}/Nodes/{folder}"
            self.nodesFolderPath[key] = value
    self.iconPaths = {}
    for folder in os.listdir(f"{self.mainDir}/imgs/icon"):
        if not os.path.isfile(f"{self.mainDir}/imgs/icon/{folder}"):
            key = folder
            value = f"{self.mainDir}/imgs/icon/{folder}"
            self.iconPaths[key] = value
    self.logoPaths = {}
    for folder in os.listdir(f"{self.mainDir}/imgs/logo"):
        if not os.path.isfile(f"{self.mainDir}/imgs/logo/{folder}"):
            key = folder
            value = f"{self.mainDir}/imgs/logo/{folder}"
            self.logoPaths[key] = value


def setMainDirectoryWinNT(self, _directory):
    self.mainDir = _directory
    self.nodesFolderPath = {}
    for folder in os.listdir(f"{self.mainDir}\\Nodes"):
        if not os.path.isfile(f"{self.mainDir}\\Nodes\\{folder}"):
            # example: "python"
            key = folder
            # example: "Release/biggusFolder/Nodes/PythonNodes"
            value = f"{self.mainDir}\\Nodes\\{folder}"
            self.nodesFolderPath[key] = value
    self.iconPaths = {}
    for folder in os.listdir(f"{self.mainDir}\\imgs\\icon"):
        if not os.path.isfile(f"{self.mainDir}\\imgs\\icon\\{folder}"):
            key = folder
            value = f"{self.mainDir}\\imgs\\icon\\{folder}"
            self.iconPaths[key] = value
    self.logoPaths = {}
    for folder in os.listdir(f"{self.mainDir}\\imgs\\logo"):
        if not os.path.isfile(f"{self.mainDir}\\imgs\\logo\\{folder}"):
            key = folder
            value = f"{self.mainDir}\\imgs\\logo\\{folder}"
            self.logoPaths[key] = value


def setBiggusConfigFile(self, _directory):
    self.configurationFilePath = f"{_directory}/config.json"


def setBiggusSaveFileDirectory(self, _directory):
    self.saveFileDirectory = _directory


def openConfigFile(self):
    print("Opening configuration file...")
    if exists("config.json"):
        print(f"Configuration file found at {os.getcwd()}\\config.json")
        with open("config.json", "r") as f:
            data = json.load(f)
    else:
        print("Configuration file not found, a new configuration file will be created.")
        openFileDialog = QFileDialog()
        openFileDialog.setFileMode(QFileDialog.Directory)
        openFileDialog.setOption(QFileDialog.ShowDirsOnly)
        if openFileDialog.exec_():
            filename = openFileDialog.selectedFiles()[0]
            with open(filename, "r") as f:
                data = json.load(f)
    self.mainDir = data["mainDir"]
    self.configurationFilePath = data["configurationFilePath"]
    self.saveFileDirectory = data["saveFileDirectory"]
    self.iconPaths = data["iconPaths"]
    self.logoPaths = data["logoPaths"]
    self.nodesFolderPath = data["nodesFolderPath"]
    configFontAndColors = data["fontAndColor"]
    for key, value in configFontAndColors.items():
        # se è un font è tipo "font": "MS Shell Dlg 2,8,-1,5,50,0,0,0,0,0",
        # se è un colore è tipo: "systemFontColor": "(250, 250, 250, 255)",
        if "Color" in key:
            # se è un colore
            value = value.replace("(", "")
            value = value.replace(")", "")
            value = value.split(",")
            # crea un q color da un rgba
            color = QColor()
            color.setRgb(int(value[0]), int(value[1]), int(value[2]), int(value[3]))
            value = QColor(color)
            self.configFontAndColors[key] = value
        else:
            # se è un font
            QFont(value)
            # font from string
            font = QFont()
            font.fromString(value)

            self.configFontAndColors[key] = font
    print(configFontAndColors)


def openConfigFileOld(self):
    print("Apertura file di configurazione...")
    try:
        with open("config.json", "r") as f:
            data = json.load(f)
    except Exception as e:
        print("File di configurazione non trovato, verrà creato un nuovo file di configurazione.")
        openDialog = QFileDialog()
        openDialog.setFileMode(QFileDialog.Directory)
        openDialog.setOption(QFileDialog.ShowDirsOnly)
        if openDialog.exec_():
            configFile = openDialog.selectedFiles()[0]
            with open(configFile, "r"):
                data = json.load(f)
        self.mainDir = data["mainDir"]
        if os.name == "nt":
            self.mainDir = data["mainDir"]
            if getattr(sys, "frozen", False):
                # Il programma è stato compilato in un eseguibile autonomo.
                # Il percorso dell'eseguibile è in sys.executable.
                print("software compilato in un eseguibile autonomo")
                self.mainDir = os.path.abspath(os.path.join(os.path.dirname(sys.executable), "biggusFolder"))
                print(f"Original main dir: {data['mainDir']}")
                print(f"New main dir: {self.mainDir}")

                biggusFolderSrc = os.path.join(self.mainDir)
                print(f"biggusFolderSrc: {biggusFolderSrc} copy to:")
                biggusTempDest = os.path.join(sys._MEIPASS, "biggusFolder")
                print(f"biggusTempDest: {biggusTempDest}")
                if shutil.copytree(biggusFolderSrc, biggusTempDest):
                    print("biggusFolder copied")
                else:
                    print("biggusFolder not copied")
            else:
                # Il programma è stato eseguito da un file sorgente.
                print("software eseguito da un file sorgente")
                self.mainDir = os.path.abspath(os.path.join(os.path.dirname(__file__), "biggusFolder"))
            module_path = self.mainDir
            os.environ["PYTHONPATH"] = os.pathsep.join([os.environ.get("PYTHONPATH", ""), module_path])
            sys.path.insert(0, module_path)

        self.configurationFilePath = data["configurationFilePath"]
        self.saveFileDirectory = data["saveFileDirectory"]
        self.iconPaths = data["iconPaths"]
        self.logoPaths = data["logoPaths"]
        self.nodesFolderPath = data["nodesFolderPath"]
        configFontAndColors = data["fontAndColor"]
        for key, value in configFontAndColors.items():
            # se è un font è tipo "font": "MS Shell Dlg 2,8,-1,5,50,0,0,0,0,0",
            # se è un colore è tipo: "systemFontColor": "(250, 250, 250, 255)",
            if "Color" in key:
                # se è un colore
                value = value.replace("(", "")
                value = value.replace(")", "")
                value = value.split(",")
                value = [int(i) for i in value]
                value = QColor(*value)
            else:
                # se è un font
                QFont(value)

        self.saveConfigFile()