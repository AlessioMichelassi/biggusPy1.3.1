from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Release.biggusFolder.tools.sliderWidgetSimple import sliderWidget


class blurTool(QWidget):
    backgroundColor: QColor = QColor(30, 31, 34)
    textColor: QColor = QColor(167, 183, 198)
    systemFont: QFont = QFont("Lohit Gujarati", 12)

    radius: sliderWidget
    sigma: sliderWidget
    grpBox: QGroupBox
    radiusChanged = pyqtSignal(str)
    sigmaChanged = pyqtSignal(str)
    valueChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.initStyle()
        self.initConnections()

    def initUI(self):
        self.grpBox = QGroupBox("BlurTool")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.grpBox)
        self.grpLayout = QVBoxLayout()
        self.grpBox.setLayout(self.grpLayout)
        self.radius = sliderWidget("Radius")
        self.sigma = sliderWidget("Sigma")
        self.grpLayout.addWidget(self.radius)
        self.grpLayout.addWidget(self.sigma)

    def initStyle(self):
        self.setFont(self.systemFont)
        style = f"""
                    QGroupBox {{
                        color: rgb({self.textColor.red()}, {self.textColor.green()}, {self.textColor.blue()});
                        background-color: rgb({self.backgroundColor.red()}, {self.backgroundColor.green()}, {self.backgroundColor.blue()});
                        border: 1px solid gray;
                        border-radius: 5px;
                        margin-top: 0.5em;
                    }}
            QGroupBox::title {{ 
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 3px;
            }}"""
        self.setStyleSheet(style)

    def initConnections(self):
        self.radius.sliderValueChange.connect(self.onSigmaChange)
        self.sigma.sliderValueChange.connect(self.onRadiusChange)

    def onRadiusChange(self, value):
        self.radiusChanged.emit(value)
        self.valueChanged.emit()

    def onSigmaChange(self, value):
        self.sigmaChanged.emit(value)
        self.valueChanged.emit()

    def setRange(self, min, max):
        self.radius.setRange(min, max)
        self.sigma.setRange(min, max)

    def setRadius(self, value):
        self.radius.setValue(value)
        self.valueChanged.emit()

    def setSigma(self, value):
        self.sigma.setValue(value)
        self.valueChanged.emit()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = blurTool()
    win.show()
    sys.exit(app.exec_())

