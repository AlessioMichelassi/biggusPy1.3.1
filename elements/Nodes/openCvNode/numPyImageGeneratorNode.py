import cv2
import numpy as np
from PyQt5.QtCore import QDir
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMenu, QFileDialog
import cv2 as cv
import sys
from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface


class numPyImageGeneratorNode(AbstractNodeInterface):
    startValue = ""
    width = 80
    height = 120
    imageWidth = 640
    imageHeight = 480
    imageColorChannel = 3
    imageDepth = np.uint8
    menuReturnValue = "blackImage"
    colorTrain = [QColor(255, 234, 242),QColor(255, 91, 110),QColor(142, 255, 242),QColor(218, 255, 251),QColor(110, 255, 91),QColor(170, 61, 73),QColor(52, 19, 23),QColor(142, 255, 242),]
    logo = r"Release/biggusFolder/imgs/logos/openCvLogo.png"

    def __init__(self, value= 20, inNum=1, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("numPyImageGenerator")
        self.setName("numPyImageGenerator")
        self.nodeGraphic.drawStripes = True
        self.changeSize(self.width, self.height)

    def calculateOutput(self, plugIndex):

        value = self.inPlugs[0].getValue()
        self.outPlugs[plugIndex].setValue(value)
        return self.outPlugs[plugIndex].getValue()

    def redesign(self):
        self.changeSize(self.width, self.height)

    def showContextMenu(self, position):
        contextMenu = QMenu()
        contextMenu.addSection("change name of menu here")
        action1 = contextMenu.addAction("blackImage")
        action2 = contextMenu.addAction("whiteImage")
        action3 = contextMenu.addAction("noiseImage")
        action4 = contextMenu.addAction("randomImage")
        action5 = contextMenu.addAction("rampImage")
        action6 = contextMenu.addAction("colorBarImage")

        action = contextMenu.exec(position)
        if action == action1:
            self.doBlackImage()
        elif action == action2:
            self.doWhiteImage()
        elif action == action3:
            self.doNoiseImage()
        elif action == action4:
            self.doRandomImage()
        elif action == action5:
            self.doRampImage()
        elif action == action6:
            self.doColorBarImage()

        if self.nodeData.outConnections:
            for connection in self.nodeData.outConnections:
                connection.updateValue()
        else:
            self.nodeData.calculate()
        self.updateAll()

    def doBlackImage(self):
        image = np.zeros((self.imageHeight, self.imageWidth, self.imageColorChannel), self.imageDepth)
        self.changeInputValue(0, image)
        return image

    def doWhiteImage(self):
        image = np.ones((self.imageHeight, self.imageWidth, self.imageColorChannel), self.imageDepth)
        image = image * 255
        self.changeInputValue(0, image)
        return image

    def doNoiseImage(self):
        image = np.random.randint(0, 255, (self.imageHeight, self.imageWidth, self.imageColorChannel), self.imageDepth)
        self.changeInputValue(0, image)
        return image

    def doRandomImage(self):
        return np.random.randint(0, 255, (self.imageHeight, self.imageWidth, self.imageColorChannel), self.imageDepth)

    def doRampImage(self):
        ramp = np.linspace(0, 255, self.imageWidth, dtype=np.float32)
        rampImage = np.tile(ramp, (self.imageHeight, 1))
        rampImage = rampImage.astype(self.imageDepth)
        self.changeInputValue(0, rampImage)
        return rampImage

    def doColorBarImage(self):
        height, width = self.imageHeight, self.imageWidth

        # Definisci i colori SMPTE come liste di valori BGR
        colorForBar = [
            [192, 192, 192],  # Grigio
            [0, 192, 192],  # Giallo
            [192, 192, 0],  # Ciano
            [0, 192, 0],  # Verde
            [192, 0, 192],  # Magenta
            [0, 0, 192],  # Rosso
            [192, 0, 0],  # Blu
            [0, 0, 0]  # Nero
        ]

        # Calcola la larghezza delle singole barre
        bar_width = width // len(colorForBar)

        # Crea un'immagine vuota con la dimensione desiderata
        smpte_image = np.zeros((height, width, 3), dtype=np.uint8)

        # Disegna le barre colorate
        for i, color in enumerate(colorForBar):
            start_x = i * bar_width
            end_x = (i + 1) * bar_width
            smpte_image[:, start_x:end_x] = color
        cv2.imwrite("color_bar_image.png", smpte_image)
        # Imposta il valore dell'input plug e restituisci l'immagine SMPTE
        self.changeInputValue(0, smpte_image)
        return smpte_image
