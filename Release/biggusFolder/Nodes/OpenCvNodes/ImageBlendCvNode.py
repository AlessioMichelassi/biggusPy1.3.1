import cv2
import numpy as np
from PyQt5.QtCore import QDir
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMenu, QFileDialog
import sys
from BiggusMain.elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface


class ImageBlendCvNode(AbstractNodeInterface):
    startValue = ""
    width = 80
    height = 120
    colorTrain = [QColor(255, 234, 242),QColor(255, 91, 110),QColor(142, 255, 242),QColor(218, 255, 251),QColor(110, 255, 91),QColor(170, 61, 73),QColor(52, 19, 23),QColor(142, 255, 242),]
    logo = r"Release/biggusFolder/imgs/logos/openCvLogo.png"

    def __init__(self, value= None, inNum=2, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("ImageBlendCvNode")
        self.setName("ImageBlendCv")
        self.nodeGraphic.drawStripes = True
        self.changeSize(self.width, self.height)
        self.menuReturnValue = "add"
        img1 = np.zeros((512, 512, 3), np.uint8)
        self.changeInputValue(0, img1, True)
        self.changeInputValue(1, img1, True)
        self.updateAll()

    def calculateOutput(self, plugIndex):
        operations = {
            "add": self.add,
            "addWeighted": self.addWeighted,
            "subtract": self.subtract,
            "multiply": self.multiply,
            "screen": self.screen,
            "overlay": self.overlay,
            "darken": self.darken,
            "lighten": self.lighten,
            "difference": self.difference,
            "exclusion": self.exclusion,
            "hardLight": self.hardLight,
            "softLight": self.softLight,
            "colorDodge": self.colorDodge,
            "colorBurn": self.colorBurn,
            "linearDodge": self.linearDodge,
            "linearBurn": self.linearBurn,
            "linearLight": self.linearLight,
            "vividLight": self.vividLight,
            "pinLight": self.pinLight,
            "hardMix": self.hardMix,
        }
        returnImage = operations[self.menuReturnValue]()
        if returnImage is None:
            return
        self.outPlugs[plugIndex].setValue(returnImage)
        self.updateAll()
        return self.outPlugs[plugIndex].getValue()

    def redesign(self):
        self.changeSize(self.width, self.height)

    def showContextMenu(self, position):
        contextMenu = QMenu()
        contextMenu.addSection("Image Blend")
        _add = contextMenu.addAction("add")
        _addWeighted = contextMenu.addAction("addWeighted")
        _subtract = contextMenu.addAction("subtract")
        _multiply = contextMenu.addAction("multiply")
        _screen = contextMenu.addAction("screen")
        _overlay = contextMenu.addAction("overlay")
        _darken = contextMenu.addAction("darken")
        _lighten = contextMenu.addAction("lighten")
        _difference = contextMenu.addAction("difference")
        _exclusion = contextMenu.addAction("exclusion")
        _hardLight = contextMenu.addAction("hardLight")
        _softLight = contextMenu.addAction("softLight")
        _colorDodge = contextMenu.addAction("colorDodge")
        _colorBurn = contextMenu.addAction("colorBurn")
        _linearDodge = contextMenu.addAction("linearDodge")
        _linearBurn = contextMenu.addAction("linearBurn")
        _linearLight = contextMenu.addAction("linearLight")
        _vividLight = contextMenu.addAction("vividLight")
        _pinLight = contextMenu.addAction("pinLight")
        _hardMix = contextMenu.addAction("hardMix")

        action = contextMenu.exec(position)
        if action:
            self.menuReturnValue = action.text()
        if action == _add:
            self.add()
        elif action == _addWeighted:
            self.addWeighted()
        elif action == _subtract:
            self.subtract()
        elif action == _multiply:
            self.multiply()
        elif action == _screen:
            self.screen()
        elif action == _overlay:
            self.overlay()
        elif action == _darken:
            self.darken()
        elif action == _lighten:
            self.lighten()
        elif action == _difference:
            self.difference()
        elif action == _exclusion:
            self.exclusion()
        elif action == _hardLight:
            self.hardLight()
        elif action == _softLight:
            self.softLight()
        elif action == _colorDodge:
            self.colorDodge()
        elif action == _colorBurn:
            self.colorBurn()
        elif action == _linearDodge:
            self.linearDodge()
        elif action == _linearBurn:
            self.linearBurn()
        elif action == _linearLight:
            self.linearLight()
        elif action == _vividLight:
            self.vividLight()
        elif action == _pinLight:
            self.pinLight()
        elif action == _hardMix:
            self.hardMix()

        if self.nodeData.outConnections:
            for connection in self.nodeData.outConnections:
                connection.updateValue()
        else:
            self.nodeData.calculate()
        self.updateAll()

    def returnImage(self):
        img1 = self.inPlugs[0].getValue()
        img2 = self.inPlugs[1].getValue()

        if img1 is None or img2 is None:
            return None, None
        if not isinstance(img1, np.ndarray) or not isinstance(img2, np.ndarray):
            return None, None
        if img1.shape != img2.shape:
            img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
        return img1, img2

    def add(self):
        img1, img2 = self.returnImage()
        if img1 is None or img2 is None:
            return
        returnImage = cv2.add(img1, img2)
        return returnImage

    def addWeighted(self):
        img1, img2 = self.returnImage()
        if img1 is None or img2 is None:
            return
        returnImage = cv2.addWeighted(img1, 0.5, img2, 0.5, 0)
        return returnImage

    def subtract(self):
        img1, img2 = self.returnImage()
        if img1 is None or img2 is None:
            return
        returnImage = cv2.subtract(img1, img2)
        return returnImage

    def multiply(self):
        img1, img2 = self.returnImage()
        if img1 is None or img2 is None:
            return
        returnImage = cv2.multiply(img1, img2)
        return returnImage

    def screen(self):
        img1, img2 = self.returnImage()
        if img1 is None or img2 is None:
            return
        img1_float = img1.astype(np.float32)
        img2_float = img2.astype(np.float32)
        returnImage = 255 - cv2.multiply(255 - img1_float, 255 - img2_float) / 255
        return returnImage.astype(np.uint8)

    def overlay2(self):
        img1, img2 = self.returnImage()
        if img1 is None or img2 is None:
            return
        result = np.zeros_like(img1)
        mask = img2 <= 128
        result[mask] = (2 * img1[mask] * img2[mask]) / 255
        result[~mask] = 255 - (2 * (255 - img1[~mask]) * (255 - img2[~mask])) / 255
        return result

    def overlay(self):
        img1, img2 = self.returnImage()
        if img1 is None or img2 is None:
            return
        result = np.where(img2 <= 128, (2 * img1 * img2) / 255, 255 - (2 * (255 - img1) * (255 - img2)) / 255)
        return result

    def darken(self):
        img1, img2 = self.returnImage()
        if img1 is None or img2 is None:
            return
        returnImage = cv2.min(img1, img2)
        return returnImage

    def lighten(self):
        img1, img2 = self.returnImage()
        if img1 is None or img2 is None:
            return
        returnImage = cv2.max(img1, img2)
        return returnImage

    def difference(self):
        img1, img2 = self.returnImage()
        if img1 is None or img2 is None:
            return
        returnImage = cv2.absdiff(img1, img2)
        return returnImage

    def exclusion(self):
        img1, img2 = self.returnImage()
        if img1 is None or img2 is None:
            return
        img1_float = img1.astype(np.float32)
        img2_float = img2.astype(np.float32)
        returnImage = img1_float + img2_float - 2 * img1_float * img2_float / 255
        return returnImage.astype(np.uint8)

    def hardLight(self):
        img1, img2 = self.returnImage()
        if img1 is None or img2 is None:
            return
        result = np.zeros_like(img1)
        mask = img1 <= 128
        result[mask] = (2 * img1[mask] * img2[mask]) / 255
        result[~mask] = 255 - (2 * (255 - img1[~mask]) * (255 - img2[~mask])) / 255
        return result

    def softLight(self):
        img1, img2 = self.returnImage()
        if img1 is None or img2 is None:
            return
        result = np.zeros_like(img1)
        mask = img2 <= 128
        result[mask] = (img1[mask] * (img2[mask] / 128)) + img1[mask] * (1 - (img2[mask] / 255))
        result[~mask] = img1[~mask] * (1 + (img2[~mask] - 128) / 128)
        return result

    def colorDodge(self):
        img1, img2 = self.returnImage()
        if img1 is None or img2 is None:
            return
        returnImage = cv2.divide(img1, cv2.bitwise_not(img2))
        return returnImage

    def colorBurn(self):
        img1, img2 = self.returnImage()
        if img1 is None or img2 is None:
            return
        returnImage = cv2.divide(cv2.bitwise_not(img1), cv2.bitwise_not(img2))
        return returnImage

    def linearDodge(self):
        img1, img2 = self.returnImage()
        if img1 is None or img2 is None:
            return
        returnImage = cv2.add(img1, img2)
        return returnImage

    def linearBurn(self):
        img1, img2 = self.returnImage()
        if img1 is None or img2 is None:
            return
        returnImage = cv2.subtract(img1, img2)
        return returnImage

    def linearLight(self):
        img1, img2 = self.returnImage()
        if img1 is None or img2 is None:
            return
        returnImage = cv2.add(img1, img2)
        return returnImage

    def vividLight(self):
        img1, img2 = self.returnImage()
        if img1 is None or img2 is None:
            return
        returnImage = cv2.add(img1, img2)
        return returnImage

    def pinLight(self):
        img1, img2 = self.returnImage()
        if img1 is None or img2 is None:
            return
        returnImage = cv2.add(img1, img2)
        return returnImage

    def hardMix(self):
        img1, img2 = self.returnImage()
        if img1 is None or img2 is None:
            return
        returnImage = cv2.add(img1, img2)
        return returnImage


