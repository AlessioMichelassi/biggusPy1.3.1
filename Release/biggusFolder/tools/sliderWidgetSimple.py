from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class sliderWidget(QWidget):
    backgroundColor: QColor = QColor(30, 31, 34)
    textColor: QColor = QColor(167, 183, 198)
    systemFont: QFont = QFont("Lohit Gujarati", 9)
    lblName: QLabel  # Name of the slider
    txtValue: QLineEdit  # Value of the slider
    sldValue: QSlider  # Slider

    sliderValueChange = pyqtSignal(str)

    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.name = name
        self.initUI()
        self.initConnections()

    def initUI(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.lblName = QLabel(self.name)
        self.lblName.setFont(self.systemFont)
        self.lblName.setStyleSheet(f"background-color: transparent; color: {self.textColor.name()};")
        self.txtValue = QLineEdit()
        self.txtValue.setValidator(QIntValidator())
        self.txtValue.setFixedWidth(50)
        self.txtValue.setFont(self.systemFont)
        self.txtValue.setStyleSheet(f"background-color: {self.backgroundColor.name()}; "
                                    f"color: {self.textColor.name()};"
                                    f"border: 1px solid {self.textColor.name()};"
                                    f"border-radius: 3px;")
        self.sldValue = QSlider(Qt.Orientation.Horizontal)
        self.layout.addWidget(self.lblName)
        self.layout.addWidget(self.sldValue)
        self.layout.addWidget(self.txtValue)

    def initConnections(self):
        self.sldValue.valueChanged.connect(self.updateValue)
        self.txtValue.textChanged.connect(self.updateSlider)

    def updateValue(self):
        self.txtValue.setText(str(self.sldValue.value()))

    def updateSlider(self):
        self.sldValue.setValue(int(self.txtValue.text()))
        self.sliderValueChange.emit(self.txtValue.text())   # Emit the signal

    def setValue(self, value):
        self.sldValue.setValue(value)
        self.txtValue.setText(str(value))

    def setRange(self, _min, _max):
        self.sldValue.setRange(_min, _max)
