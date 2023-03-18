from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import cv2
import psutil
import time

from BiggusMain.elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface

"""
https://stackoverflow.com/questions/11420748/setting-camera-parameters-in-opencv-python
0. CV_CAP_PROP_POS_MSEC Current position of the video file in milliseconds.
1. CV_CAP_PROP_POS_FRAMES 0-based index of the frame to be decoded/captured next.
2. CV_CAP_PROP_POS_AVI_RATIO Relative position of the video file
3. CV_CAP_PROP_FRAME_WIDTH Width of the frames in the video stream.
4. CV_CAP_PROP_FRAME_HEIGHT Height of the frames in the video stream.
5. CV_CAP_PROP_FPS Frame rate.
6. CV_CAP_PROP_FOURCC 4-character code of codec.
7. CV_CAP_PROP_FRAME_COUNT Number of frames in the video file.
8. CV_CAP_PROP_FORMAT Format of the Mat objects returned by retrieve() .
9. CV_CAP_PROP_MODE Backend-specific value indicating the current capture mode.
10. CV_CAP_PROP_BRIGHTNESS Brightness of the image (only for cameras).
11. CV_CAP_PROP_CONTRAST Contrast of the image (only for cameras).
12. CV_CAP_PROP_SATURATION Saturation of the image (only for cameras).
13. CV_CAP_PROP_HUE Hue of the image (only for cameras).
14. CV_CAP_PROP_GAIN Gain of the image (only for cameras).
15. CV_CAP_PROP_EXPOSURE Exposure (only for cameras).
16. CV_CAP_PROP_CONVERT_RGB Boolean flags indicating whether images should be converted to RGB.
17. CV_CAP_PROP_WHITE_BALANCE Currently unsupported
18. CV_CAP_PROP_RECTIFICATION Rectification flag for stereo cameras (note: only supported by DC1394 v 2.x backend currently)

(Please note, as commenter Markus Weber pointed out below, in OpenCV 4 you have to remove the "CV" prefix from the property name, eg cv2.CV_CAP_PROP_FRAME_HEIGHT -> cv2.CAP_PROP_FRAME_HEIGHT)
"""

class blinker(QWidget):
    lblBlink: QLabel
    lblImage: QLabel

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.lblBlink = QLabel(self)
        self.lblBlink.setFixedSize(20, 10)
        layout = QVBoxLayout()
        layout.addWidget(self.lblBlink, 0, Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(2, 2, 2, 2)
        self.setStyleSheet("background-color: transparent; border: 1px solid black; border-radius: 2px;")
        self.setLayout(layout)

    def doBlinking(self, blink):
        if blink:
            style = "QLabel { background-color : red; }"
        else:
            style = "QLabel { background-color : rgb(10,10,10); }"
        self.lblBlink.setStyleSheet(style)


class CameraWorker(QThread):
    frame_ready = pyqtSignal(object)
    cpuUsageHigh = pyqtSignal(str)
    frameRate = pyqtSignal(str)
    cameraInfo = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.cam = cv2.VideoCapture(0)
        self.frame = None
        self._stopped = False
        self._slow_down = False
        self.cpuUsageThreshold = 60

    def setFrameRate(self, frameRate):
        self.cam.set(cv2.CAP_PROP_FPS, frameRate)

    def getFrameRate(self):
        return str(self.cam.get(cv2.CAP_PROP_FPS))

    def setResolution(self, width, height):
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def getResolution(self):
        return self.cam.get(cv2.CAP_PROP_FRAME_WIDTH), self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def setHalfResolution(self):
        width, height = self.getResolution()
        self.setResolution(int(width / 2), int(height / 2))

    def printCameraInfo(self):
        framerate = self.cam.get(cv2.CAP_PROP_FPS)
        fpsCount = self.cam.get(cv2.CAP_PROP_FRAME_COUNT)
        posFrames = self.cam.get(cv2.CAP_PROP_POS_FRAMES)
        width = self.cam.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
        cameraInfo = f"Camera Info:\n\tFramerate: {framerate}\n\tFPS Count: {fpsCount}\n\tPos Frames: {posFrames}\n\tWidth: {width}\n\tHeight: {height}"
        self.cameraInfo.emit(cameraInfo)

    def run(self):
        while not self._stopped:
            self.printCameraInfo()
            if not self._slow_down:  # Aggiungi questo controllo
                ret, self.frame = self.cam.read()
                if ret:
                    self.frame_ready.emit(self.frame)
                    self.frameRate.emit(self.getFrameRate())
                else:
                    time.sleep(0.1)
            cpu_percent = psutil.cpu_percent()  # Ottieni l'utilizzo della CPU in percentuale
            if cpu_percent > self.cpuUsageThreshold:
                print("CPU usage is high: ", cpu_percent)
                self.cpuUsageHigh.emit(str(cpu_percent))
                self.setFrameRate(1)
                self.setHalfResolution()
                self._slow_down = True  # Rallenta la cattura dei fotogrammi
            else:
                self._slow_down = False  # Riprendi la cattura dei fotogrammi al ritmo normale

    def stop(self):
        self._stopped = True
        self.wait()
        self.cam.release()


class VideoCVCameraNode(AbstractNodeInterface):
    startValue = 0
    width = 50
    height = 120
    colorTrain = [QColor(255, 234, 242), QColor(255, 91, 110), QColor(142, 255, 242), QColor(218, 255, 251),
                  QColor(110, 255, 91), QColor(170, 61, 73), QColor(52, 19, 23), QColor(142, 255, 242)]
    logo = r"Release/biggusFolder/imgs/logos/openCvLogo.png"
    videoCamera: CameraWorker
    proxyWidget: blinker
    lblCamera: QLabel
    isBlinking = False
    timer = QTimer()

    def __init__(self, value="uriFile", inNum=1, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("VideoCVCameraNode")
        self.setName("VideoCameraNode")
        self.nodeGraphic.drawStripes = True
        self.nodeGraphic.drawStripes = True
        self.changeSize(self.width, self.height)
        self.AddProxyWidget()
        self.addLabelProxyWidget()
        self.videoCamera = None
        self.frameImage = QImage()
        self.lastFrame = None

    def calculateOutput(self, plugIndex):
        value = self.inPlugs[0].getValue()
        self.outPlugs[plugIndex].setValue(value)
        return self.outPlugs[plugIndex].getValue()

    def process_frames(self, frame):
        self.changeInputValue(0, frame)
        self.calculateOutput(0)
        # visualizza il frame nel widget proxy
        height, width, channel = frame.shape
        bytesPerLine = 3 * width
        qImg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
        return QPixmap.fromImage(qImg)

    def startVideoCamera(self):
        self.videoCamera = CameraWorker()  # Cambio dell'istanza con il thread
        self.videoCamera.frame_ready.connect(self.process_frames)
        self.videoCamera.cpuUsageHigh.connect(self.onCpuUsageHigh)
        self.videoCamera.frameRate.connect(self.onFrameRate)
        self.videoCamera.cameraInfo.connect(self.showCameraInfo)
        self.videoCamera.start()

    def stopVideoCamera(self):
        self.videoCamera.stop()
        self.videoCamera = None

    def onCpuUsageHigh(self, cpuUsage):
        # rallenta il framerate della camera
        self.videoCamera.setFrameRate(1)
        self.proxyWidget.doBlinking(False)
        self.lblCamera.setText(f"W: {cpuUsage}")

    def onFrameRate(self, frameRate):
        self.lblCamera.setText(f"{str(frameRate)}")

    def redesign(self):
        self.changeSize(self.width, self.height)

    def updateAll(self):
        super().updateAll()
        self.isBlinking = not self.isBlinking
        self.proxyWidget.doBlinking(self.isBlinking)

    def AddProxyWidget(self):
        self.proxyWidget = blinker()
        self.nodeGraphic.createProxyWidget(self.proxyWidget)
        self.proxyWidget.setFixedWidth(self.width - 20)
        self.proxyWidget.setFixedHeight(20)
        self.proxyWidget.move(int(self.width // 2 - self.proxyWidget.width() // 2),
                              int(self.height - 30))

    def addLabelProxyWidget(self):
        self.lblCamera = QLabel("fps: 0")
        self.nodeGraphic.create2ndProxyWidget(self.lblCamera)
        self.lblCamera.setFixedWidth(self.width - 20)
        self.lblCamera.setFixedHeight(20)
        self.lblCamera.setStyleSheet("font-size: 6px; color: black; "
                                     "background-color: transparent; ")
        self.lblCamera.move(int(self.width // 2 - self.lblCamera.width() // 2), 50)

    def onClose(self):
        # Stop al worker del thread
        self.videoCamera.stop()
        super().onClose()

    def showContextMenu(self, position):
        menu = QMenu()
        action1 = menu.addAction("Start")
        action2 = menu.addAction("Save Video As")
        action3 = menu.addAction("Stop")

        action = menu.exec_(position)
        if action == action1:
            if self.videoCamera is None or not self.videoCamera.isRunning():
                self.startVideoCamera()
        elif action == action2:
            print("Save Video As")
        elif action == action3:
            if self.videoCamera is not None and self.videoCamera.isRunning():
                self.stopVideoCamera()

    def showCameraInfo(self, info):
        print(info)
