import json
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class dirChooser(QWidget):
    lblFolderDirectory: QLabel
    btnChooseDirectory: QPushButton
    lneBiggusDirectory: QLineEdit

    directoryChanged = pyqtSignal(str)
    dirPath = "BiggusMain/elements/imgs/blue-folder-horizontal.png"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUi()
        self.initConnection()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def initUi(self):
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)
        lblLayout = self.initLabel()
        btnLayout = self.initButton()
        mainLayout.addLayout(lblLayout)
        mainLayout.addLayout(btnLayout)

    def initLabel(self):
        self.lblFolderDirectory = QLabel(self)
        self.lblFolderDirectory.setObjectName("lblFolderDirectory")
        self.lblFolderDirectory.setText("Biggus Directory")
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        lblLayout = QHBoxLayout()
        lblLayout.addWidget(self.lblFolderDirectory)
        lblLayout.addItem(spacer)
        return lblLayout

    def initButton(self):
        self.btnChooseDirectory = QPushButton(self)
        path = os.path.join(self.dirPath)
        if os.path.exists(path):
            self.btnChooseDirectory.setIcon(QIcon(path))
        else:
            print("Path not found")
        self.btnChooseDirectory.setObjectName("btnChooseDirectory")
        self.lneBiggusDirectory = QLineEdit(self)
        self.lneBiggusDirectory.setObjectName("lneBiggusDirectory")
        self.btnChooseDirectory.setFixedSize(self.lneBiggusDirectory.height(), 30)
        btnLayout = QHBoxLayout()
        btnLayout.addWidget(self.btnChooseDirectory)
        btnLayout.addWidget(self.lneBiggusDirectory)
        return btnLayout

    def initConnection(self):
        self.btnChooseDirectory.clicked.connect(self.chooseDirectory)
        # on returnPressed
        self.lneBiggusDirectory.returnPressed.connect(self.onDirectoryChanged)

    def setName(self, name: str):
        self.lblFolderDirectory.setText(name)
        self.update()

    def setInitialLocation(self, location: str):
        self.lneBiggusDirectory.setText(location)
        self.update()

    def getDirectory(self):
        return self.lneBiggusDirectory.text()

    def setDirectory(self, directory: str):
        self.lneBiggusDirectory.setText(directory)

    def chooseDirectory(self):
        directory = QFileDialog.getExistingDirectory(self, "Choose Directory", self.lneBiggusDirectory.text())
        if directory:
            self.lneBiggusDirectory.setText(directory)

    def onDirectoryChanged(self, text: str):
        self.directoryChanged.emit(text)


class fileChooser(QWidget):
    lblFile: QLabel
    btnChooseFile: QPushButton
    lneFile: QLineEdit
    fileChanged = pyqtSignal(str)
    dirFile = "BiggusMain/elements/imgs/blue-folder-horizontal.png"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUi()
        self.initConnection()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def initUi(self):
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)
        lblLayout = self.initLabel()
        btnLayout = self.initButton()
        mainLayout.addLayout(lblLayout)
        mainLayout.addLayout(btnLayout)

    def initLabel(self):
        self.lblFile = QLabel(self)
        self.lblFile.setObjectName("lblFile")
        self.lblFile.setText("File")
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        lblLayout = QHBoxLayout()
        lblLayout.addWidget(self.lblFile)
        lblLayout.addItem(spacer)
        return lblLayout

    def initButton(self):
        self.btnChooseFile = QPushButton(self)
        self.btnChooseFile.setIcon(QIcon(self.dirFile))
        self.btnChooseFile.setObjectName("btnChooseFile")
        self.lneFile = QLineEdit(self)
        self.lneFile.setObjectName("lneFile")
        self.btnChooseFile.setFixedSize(self.lneFile.height(), 30)
        btnLayout = QHBoxLayout()
        btnLayout.addWidget(self.btnChooseFile)
        btnLayout.addWidget(self.lneFile)
        return btnLayout

    def initConnection(self):
        self.btnChooseFile.clicked.connect(self.chooseFile)
        self.lneFile.textChanged.connect(self.onFileChanged)

    def setName(self, name: str):
        self.lblFile.setText(name)
        self.update()

    def chooseFile(self):
        file = QFileDialog.getOpenFileName(self, "Choose File", self.lneFile.text())
        if file:
            self.lneFile.setText(file[0])

    def onFileChanged(self, text: str):
        self.fileChanged.emit(text)

    def setInitialLocation(self, location: str):
        self.lneFile.setText(location)
        self.update()


class fontChooser(QWidget):
    lblFont: QLabel
    btnChooseFont: QPushButton
    lneFont: QLineEdit
    fontChanged = pyqtSignal(str)
    font: QFont
    dirFont = "BiggusMain/elements/imgs/font-64.png"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUi()
        self.initConnection()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def initUi(self):
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)
        lblLayout = self.initLabel()
        btnLayout = self.initButton()
        mainLayout.addLayout(lblLayout)
        mainLayout.addLayout(btnLayout)

    def initLabel(self):
        self.lblFont = QLabel(self)
        self.lblFont.setObjectName("lblFont")
        self.lblFont.setText("Font")
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        lblLayout = QHBoxLayout()
        lblLayout.addWidget(self.lblFont)
        lblLayout.addItem(spacer)
        return lblLayout

    def initButton(self):
        self.btnChooseFont = QPushButton(self)
        self.btnChooseFont.setIcon(QIcon(self.dirFont))
        self.btnChooseFont.setObjectName("btnChooseFont")
        self.lneFont = QLineEdit(self)
        self.lneFont.setObjectName("lneFont")
        self.btnChooseFont.setFixedSize(self.lneFont.height(), 30)
        btnLayout = QHBoxLayout()
        btnLayout.addWidget(self.btnChooseFont)
        btnLayout.addWidget(self.lneFont)
        return btnLayout

    def initConnection(self):
        self.btnChooseFont.clicked.connect(self.chooseFont)
        self.lneFont.textChanged.connect(self.onFontChanged)

    def setName(self, name: str):
        fontToolTip = self.fontToolTips()
        self.lblFont.setToolTip(fontToolTip)
        self.lblFont.setText(name)
        self.update()

    def fontToolTips(self):
        # font-family:font-size:font-weight:font-style:font-stretch:font-underline:font-overline:font-strikeout:font-kerning:font-capitalization:font-letterspacing:font-wordspacing
        return "f-family, size, weight, stretch, underline, overline, strikeout, kerning, capitalization, " \
               "letterspacing, wordspacing"

    def setInitialFont(self, font: QFont):
        if isinstance(font, str):
            self.font.fromString(font)
            self.lneFont.setText(font)
        elif isinstance(font, QFont):
            self.font = font
            fontToString = font.toString()
            self.lneFont.setText(fontToString)
        self.update()

    def getFont(self):
        return self.font

    def setFont(self, font: str):
        if isinstance(font, str):
            self.font.fromString(font)
            self.lneFont.setText(font)
        elif isinstance(font, QFont):
            self.font = font
            self.lneFont.setText(font.toString())

    def chooseFont(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.font = font
            self.lneFont.setText(font.toString())

    def onFontChanged(self, text: str):
        self.fontChanged.emit(text)


class colorChooser(QWidget):
    lblColor: QLabel
    btnChooseColor: QPushButton
    lneColorHex: QLineEdit
    lneColorRGB: QLineEdit
    lneColorHUE: QLineEdit
    lblColorShow: QLabel
    colorChanged = pyqtSignal(str)
    color: QColor
    iconFolder = "BiggusMain/elements/imgs/color.png"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUi()
        self.initConnection()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def initUi(self):
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)
        lblLayout = self.initLabel()
        btnLayout = self.initButton()
        mainLayout.addLayout(lblLayout)
        mainLayout.addLayout(btnLayout)

    def initLabel(self):
        self.lblColor = QLabel(self)
        self.lblColor.setObjectName("lblColor")
        self.lblColor.setText("Color")
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        lblLayout = QHBoxLayout()
        lblLayout.addWidget(self.lblColor)
        lblLayout.addItem(spacer)
        return lblLayout

    def initButton(self):
        self.btnChooseColor = QPushButton(self)
        self.btnChooseColor.setIcon(QIcon(self.iconFolder))
        self.btnChooseColor.setObjectName("btnChooseColor")
        self.lneColorHex = QLineEdit(self)
        self.lneColorHex.setObjectName("lneColorHex")
        self.lblColorShow = QLabel(self)
        self.lblColorShow.setFixedSize(20, 20)
        self.lneColorRGB = QLineEdit(self)
        self.lneColorRGB.setObjectName("lneColorRGB")
        self.lneColorHUE = QLineEdit(self)
        self.lneColorHUE.setObjectName("lneColorHUE")
        self.btnChooseColor.setFixedSize(self.lneColorHUE.height(), 40)
        btnLayout = QHBoxLayout()
        btnLayout.addWidget(self.btnChooseColor)
        lblHex = QLabel("hex")
        btnLayout.addWidget(lblHex)
        btnLayout.addWidget(self.lneColorHex)
        lblRgb = QLabel("rgb")
        btnLayout.addWidget(lblRgb)
        btnLayout.addWidget(self.lneColorRGB)
        lblHue = QLabel("hue")
        btnLayout.addWidget(lblHue)
        btnLayout.addWidget(self.lneColorHUE)
        btnLayout.addWidget(self.lblColorShow)
        return btnLayout

    def initConnection(self):
        self.btnChooseColor.clicked.connect(self.chooseColor)
        self.lneColorHex.textChanged.connect(self.onColorChanged)

    def setName(self, name: str):
        self.lblColor.setText(name)
        self.update()

    def setInitialColor(self, color):
        if isinstance(color, str):
            _color = QColor(color)
            self.returnColorOnAllLineEdit(_color)
        elif isinstance(color, QColor):
            self.returnColorOnAllLineEdit(color)
        self.update()

    def getColor(self):
        return self.color

    def setColor(self, color: str):
        if isinstance(color, str):
            _color = QColor(color)
            self.returnColorOnAllLineEdit(_color)
        elif isinstance(color, QColor):
            self.returnColorOnAllLineEdit(color)

    def returnColorOnAllLineEdit(self, arg0):
        self.color = arg0
        self.lneColorHex.setText(arg0.name())
        self.lneColorRGB.setText(arg0.getRgb().__str__())
        self.lneColorHUE.setText(arg0.getHsl().__str__())
        self.lblColorShow.setStyleSheet(f"background-color: {arg0.name()}")

    def chooseColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.returnColorOnAllLineEdit(color)

    def onColorChanged(self, text: str):
        self.colorChanged.emit(text)


class PreferenceWidget(QWidget):
    tabWidget: QTabWidget
    tabSystemSettings: QWidget
    tabSystemSettings2: QWidget
    btnSaveSettings: QPushButton
    grpBoxSystemDir: QGroupBox
    grpBoxSystemFont: QGroupBox

    biggusDirChooser: dirChooser
    biggusConfigFile: fileChooser
    biggusSaveFileDir: dirChooser

    biggusSystemFontChooser: fontChooser
    biggusWidgetFontChooser: fontChooser
    biggusWidgetOnWidgetFontChooser: fontChooser

    biggusSystemFontColorChooser: colorChooser
    biggusSystemBackgroundColorChooser: colorChooser
    biggusSystemBorderColorChooser: colorChooser

    biggusWidgetFontColorChooser: colorChooser
    biggusWidgetBackgroundColorChooser: colorChooser
    biggusWidgetBorderColorChooser: colorChooser

    biggusWidgetOnWidgetFontColorChooser: colorChooser
    biggusWidgetOnWidgetBackgroundColorChooser: colorChooser
    biggusWidgetOnWidgetBorderColorChooser: colorChooser

    def __init__(self, biggusPy, parent=None):
        super().__init__(parent)
        self.biggusPy = biggusPy
        self.initUi()
        self.initConnection()
        self.initStyle()

    def initUi(self):
        self.tabWidget = QTabWidget(self)
        self.initTabWidget()
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.tabWidget)
        self.btnSaveSettings = QPushButton("Save Settings")

        mainLayout.addWidget(self.btnSaveSettings)
        self.setLayout(mainLayout)

    def initTabWidget(self):
        self.tabSystemSettings = QWidget()
        layout = QVBoxLayout()
        self.tabSystemSettings.setLayout(layout)
        self.tabSystemSettings.setObjectName("tabSystemSettings")
        self.grpBoxSystemDir = self.initGrpSystemBox()
        layout.addWidget(self.grpBoxSystemDir)
        self.grpBoxSystemFont = self.initGrpBoxSystemFont()
        layout.addWidget(self.grpBoxSystemFont)
        self.tabWidget.addTab(self.tabSystemSettings, "Preferences")

    def initGrpSystemBox(self):
        grpBoxSystem = QGroupBox(self.tabSystemSettings)
        grpBoxSystem.setObjectName("grpBoxSystem")
        grpBoxSystem.setTitle("System Settings")
        grpBoxSystem.setLayout(QVBoxLayout())
        self.biggusDirChooser = self.returnDirectoryChooser("Biggus Directory", self.biggusPy.mainDir)
        self.biggusConfigFile = self.returnFileChooser("Biggus Config File", self.biggusPy.configurationFilePath)
        self.biggusSaveFileDir = self.returnDirectoryChooser("Biggus Save File Directory", self.biggusPy.saveFileDirectory)
        grpBoxSystem.layout().addWidget(self.biggusDirChooser)
        grpBoxSystem.layout().addWidget(self.biggusConfigFile)
        grpBoxSystem.layout().addWidget(self.biggusSaveFileDir)
        # spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # grpBoxSystem.layout().addItem(spacer)
        return grpBoxSystem

    def initGrpBoxSystemFont(self):
        grpBoxSystemFont = QGroupBox(self.tabSystemSettings)
        grpBoxSystemFont.setObjectName("grpBoxSystemFont")
        grpBoxSystemFont.setTitle("System Color")
        grpBoxSystemFont.setLayout(QVBoxLayout())
        self.biggusSystemFontChooser = self.returnFontChooser("System Font",
                                                              self.biggusPy.configFontAndColors["systemFont"])
        grpBoxSystemFont.layout().addWidget(self.biggusSystemFontChooser)
        self.biggusWidgetFontChooser = self.returnFontChooser("Widget Font",
                                                              self.biggusPy.configFontAndColors["widgetFont"])
        grpBoxSystemFont.layout().addWidget(self.biggusWidgetFontChooser)
        self.biggusWidgetOnWidgetFontChooser = self.returnFontChooser("Widget On Widget Font",
                                                                      self.biggusPy.configFontAndColors[
                                                                          "widgetOnWidgetFont"])
        grpBoxSystemFont.layout().addWidget(self.biggusWidgetOnWidgetFontChooser)

        self.biggusSystemFontColorChooser = self.returnColorChooser("System Font Color",
                                                                    self.biggusPy.configFontAndColors[
                                                                        "systemFontColor"])
        grpBoxSystemFont.layout().addWidget(self.biggusSystemFontColorChooser)
        self.biggusSystemBackgroundColorChooser = self.returnColorChooser("System Background Color",
                                                                          self.biggusPy.configFontAndColors[
                                                                              "systemBackgroundColor"])
        grpBoxSystemFont.layout().addWidget(self.biggusSystemBackgroundColorChooser)
        self.biggusSystemBorderColorChooser = self.returnColorChooser("System Border Color",
                                                                      self.biggusPy.configFontAndColors[
                                                                          "systemBorderColor"])
        grpBoxSystemFont.layout().addWidget(self.biggusSystemBorderColorChooser)

        self.biggusWidgetFontColorChooser = self.returnColorChooser("Widget Font Color",
                                                                    self.biggusPy.configFontAndColors[
                                                                        "widgetFontColor"])
        grpBoxSystemFont.layout().addWidget(self.biggusWidgetFontColorChooser)
        self.biggusWidgetBackgroundColorChooser = self.returnColorChooser("Widget Background Color",
                                                                          self.biggusPy.configFontAndColors[
                                                                              "widgetBackgroundColor"])
        grpBoxSystemFont.layout().addWidget(self.biggusWidgetBackgroundColorChooser)
        self.biggusWidgetBorderColorChooser = self.returnColorChooser("Widget Border Color",
                                                                      self.biggusPy.configFontAndColors[
                                                                          "widgetBorderColor"])
        grpBoxSystemFont.layout().addWidget(self.biggusWidgetBorderColorChooser)

        self.biggusWidgetOnWidgetFontColorChooser = self.returnColorChooser("Widget On Widget Font Color",
                                                                            self.biggusPy.configFontAndColors[
                                                                                "widgetOnWidgetFontColor"])
        grpBoxSystemFont.layout().addWidget(self.biggusWidgetOnWidgetFontColorChooser)
        self.biggusWidgetOnWidgetBackgroundColorChooser = self.returnColorChooser("Widget On Widget Background Color",
                                                                                  self.biggusPy.configFontAndColors[
                                                                                      "widgetOnWidgetBackgroundColor"])
        grpBoxSystemFont.layout().addWidget(self.biggusWidgetOnWidgetBackgroundColorChooser)
        self.biggusWidgetOnWidgetBorderColorChooser = self.returnColorChooser("Widget On Widget Border Color",
                                                                              self.biggusPy.configFontAndColors[
                                                                                  "widgetOnWidgetBorderColor"])
        grpBoxSystemFont.layout().addWidget(self.biggusWidgetOnWidgetBorderColorChooser)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        grpBoxSystemFont.layout().addItem(spacer)
        return grpBoxSystemFont

    @staticmethod
    def returnDirectoryChooser(name, initialLocation):
        result = dirChooser()
        result.setName(name)
        result.setInitialLocation(initialLocation)
        return result

    @staticmethod
    def returnFileChooser(name, initialLocation):
        result = fileChooser()
        result.setName(name)
        result.setInitialLocation(initialLocation)
        return result

    @staticmethod
    def returnFontChooser(name, initialFont):
        result = fontChooser()
        result.setName(name)
        result.setInitialFont(initialFont)
        return result

    @staticmethod
    def returnColorChooser(name, initialColor):
        result = colorChooser()
        result.setName(name)
        result.setInitialColor(initialColor.name())
        return result

    def initConnection(self):
        self.btnSaveSettings.clicked.connect(self.saveSettings)
        self.biggusDirChooser.directoryChanged.connect(self.setBiggusDir)
        self.biggusConfigFile.fileChanged.connect(self.setBiggusConfigFile)
        self.biggusSaveFileDir.directoryChanged.connect(self.setBiggusSaveFileDir)

    def saveSettings(self):
        self.biggusPy.saveConfigFile()
        self.close()

    def setBiggusDir(self, _dir):
        self.biggusPy.setMainDirectory(_dir)

    def setBiggusConfigFile(self, filePath):
        self.biggusPy.configurationFilePath = filePath
        self.biggusPy.openConfigFile()

    def setBiggusSaveFileDir(self, _dir):
        self.biggusPy.setSaveFileDir(_dir)

    # ------------------ Style ------------------

    def initStyle(self):
        # i colori sono settati rgb
        # il titole della grpBox è allineato al centro
        style = f""" 
        QWidget {{
            background-color: rgb({self.biggusPy.configFontAndColors["systemBackgroundColor"].red()}, {self.biggusPy.configFontAndColors["systemBackgroundColor"].green()}, {self.biggusPy.configFontAndColors["systemBackgroundColor"].blue()});
            color: rgb({self.biggusPy.configFontAndColors["systemFontColor"].red()}, {self.biggusPy.configFontAndColors["systemFontColor"].green()}, {self.biggusPy.configFontAndColors["systemFontColor"].blue()});
            font: {self.biggusPy.configFontAndColors["systemFont"].family()};
            font-size: {self.biggusPy.configFontAndColors["systemFont"].pointSize()}px;
        }}
        QGroupBox {{
            background-color: rgb({self.biggusPy.configFontAndColors["widgetBackgroundColor"].red()}, {self.biggusPy.configFontAndColors["widgetBackgroundColor"].green()}, {self.biggusPy.configFontAndColors["widgetBackgroundColor"].blue()});
            border: 1px solid rgb({self.biggusPy.configFontAndColors["widgetBorderColor"].red()}, {self.biggusPy.configFontAndColors["widgetBorderColor"].green()}, {self.biggusPy.configFontAndColors["widgetBorderColor"].blue()});
            border-radius: 5px;
            margin-top: 1ex;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 3px;
            background-color: rgb({self.biggusPy.configFontAndColors["widgetBackgroundColor"].red()}, {self.biggusPy.configFontAndColors["widgetBackgroundColor"].green()}, {self.biggusPy.configFontAndColors["widgetBackgroundColor"].blue()});
            color: rgb({self.biggusPy.configFontAndColors["widgetFontColor"].red()}, {self.biggusPy.configFontAndColors["widgetFontColor"].green()}, {self.biggusPy.configFontAndColors["widgetFontColor"].blue()});
            font: {self.biggusPy.configFontAndColors["widgetFont"].family()};
            font-size: {self.biggusPy.configFontAndColors["widgetFont"].pointSize()}px;
        }}
        QLabel {{
            background-color: transparent;
            }}
        """
        self.setStyleSheet(style)
