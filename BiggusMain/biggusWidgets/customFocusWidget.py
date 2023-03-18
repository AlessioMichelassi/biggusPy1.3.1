from PyQt5.QtCore import Qt, QObject, QEvent
from PyQt5.QtGui import QKeyEvent, QPainter, QColor, QPen, QFocusEvent
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, QGraphicsView, QApplication, QGraphicsProxyWidget

"""
ITA:
    Questa classe è un widget che può essere selezionato con il click del mouse.
    Quando è selezionato, viene disegnato un bordo rosso. In questo modo è possibile
    distinguere i vari widget e soprattutto gestire il fuoco per il tasto tab.
    
    Inoltre, quando viene premuto il tasto tab, il fuoco rimane sul widget e non viene
    passato al widget successivo. Questo perchè ogni widget ha il suo tab implementato.
    
    Per abilitare il debug del fuoco, impostare la variabile isDebugFocus a True.

ENG:
    This class is a widget that can be selected with the mouse click.
    When it is selected, a red border is drawn. In this way it is possible
    to distinguish the various widgets and above all to manage the focus for the tab key.
    
    In addition, when the tab key is pressed, the focus remains on the widget and is not
    passed to the next widget. This is because each widget has its own tab implemented.
    
    To enable the focus debug, set the isDebugFocus variable to True.
"""


class customFocusWidget(QWidget):
    isDebugFocus = False
    systemWidgetFont = "Lohit Gujarati"
    systemWidgetFontSize = 8
    systemWidgetTextColor = "black"
    systemWidgetColor = "white"
    systemWidgetBorderColor = "black"
    systemWidgetBackGroundColor = "white"

    def __init__(self, biggusPy, parent=None):
        super().__init__(parent)
        self.biggusPy = biggusPy
        self.getWidgetStyleFromBiggus()
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.setMouseTracking(True)
        self.isWidgetSelected = False
        self.installEventFilter(self)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        # sourcery skip: extract-duplicate-method
        if event.type() == QEvent.Type.FocusIn:
            if self.isDebugFocus:
                print("FocusIn from", watched, "to", self)
            self.isWidgetSelected = True
            self.update()
        elif event.type() == QEvent.Type.FocusOut:
            if self.isDebugFocus:
                print("FocusOut from", watched, "to", self)
            self.isWidgetSelected = False
            self.update()
        return super().eventFilter(watched, event)

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.isWidgetSelected:
            painter.setPen(QPen(QColor(120, 60, 30), 2, Qt.PenStyle.SolidLine))
        else:
            painter.setPen(QPen(QColor(10, 10, 10), 1, Qt.PenStyle.SolidLine))
        painter.drawRoundedRect(self.rect(), 5, 5)

    def event(self, event: QEvent) -> bool:
        if event.type() == QEvent.Type.MouseButtonPress:
            # when the mouse is clicked, the focus is set on the widget
            self.setFocus()
        if event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Tab:
                # when the tab key is pressed, the focus remains on the widget
                # and is not passed to the next widget
                # because each widget has its own tab implemented
                self.keyPressEvent(event)
                return True
        return super().event(event)

    def setWidgetStyle(self):
        self.setStyleSheet(
            f"""
            QWidget {{
                background-color: rgba({self.systemWidgetBackGroundColor.red()}, {self.systemWidgetBackGroundColor.green()}, {self.systemWidgetBackGroundColor.blue()}, {self.systemWidgetBackGroundColor.alpha()});
                color: rgba({self.systemWidgetTextColor.red()}, {self.systemWidgetTextColor.green()}, {self.systemWidgetTextColor.blue()}, {self.systemWidgetTextColor.alpha()});
                font-family: {self.systemWidgetFont};
                font-size: {self.systemWidgetFontSize}px;
            }}""")

    def getWidgetStyleFromBiggus(self):
        font = self.biggusPy.systemWidgetFont
        if isinstance(font, str):
            self.systemWidgetFont = font
            self.systemWidgetFontSize = self.biggusPy.systemWidgetFontSize
        else:
            self.systemWidgetFont = font.family()
            self.systemWidgetFontSize = font.pointSize()

        self.systemWidgetTextColor = self.biggusPy.systemWidgetFontColor
        self.systemWidgetColor = self.biggusPy.systemWidgetFontColor
        self.systemWidgetBorderColor = self.biggusPy.systemWidgetBorderColor
        self.systemWidgetBackGroundColor = self.biggusPy.systemWidgetBackGroundColor
        self.setWidgetStyle()
