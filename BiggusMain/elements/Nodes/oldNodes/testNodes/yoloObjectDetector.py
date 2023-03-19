import cv2

from PyQt5.QtCore import QDir
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMenu, QFileDialog
import cv2 as cv
import sys
from BiggusMain.elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface
try:
    import torch
    import torchvision
    from torch import hub
except:
    print(f"Error opening yolo ObjectDetector node, torch.hub not found\npip install torch")


class yoloObjectDetector(AbstractNodeInterface):
    startValue = ""
    width = 80
    height = 120
    colorTrain = [QColor(255, 234, 242), QColor(255, 91, 110), QColor(142, 255, 242), QColor(218, 255, 251),
                  QColor(110, 255, 91), QColor(170, 61, 73), QColor(52, 19, 23), QColor(142, 255, 242), ]
    logo = r"Release/biggusFolder/imgs/logos/openCvLogo.png"

    def __init__(self, value=20, inNum=2, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("CvNode")
        self.setName("CvNode")
        self.changeSize(self.width, self.height)
        self.model = hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True, trust_repo=True)

    def calculateOutput(self, plugIndex):
        value = self.inPlugs[0].getValue()
        if value is None:
            return
        self.cam = cv2.VideoCapture(0)
        ret, frame = self.cam.read()
        result = self.score_frame(frame, self.model)
        frame = self.plot_boxes(result, frame)
        self.outPlugs[plugIndex].setValue(frame)
        return self.outPlugs[plugIndex].getValue()
    def redesign(self):
        self.changeSize(self.width, self.height)

    def showContextMenu(self, position):
        contextMenu = QMenu()
        contextMenu.addSection("change name of menu here")
        action1 = contextMenu.addAction("action1")
        action2 = contextMenu.addAction("action2")
        action3 = contextMenu.addAction("action3")

        action = contextMenu.exec(position)
        if action == action1:
            self.doAction1()
        elif action == action2:
            self.doAction2()
        elif action == action3:
            self.doAction3()

    def doAction1(self):
        pass

    def doAction2(self):
        pass

    def doAction3(self):
        pass

    def score_frame(self, frame, model):
        """
        ENG: The function below identifies the device which is availabe to make the prediction and uses it to load and
        infer the frame. Once it has results it will extract the labels and cordinates(Along with scores) for each object
        detected in the frame.
        ITA:
        Questa funzione identifica il dispositivo disponibile per effettuare la predizione event lo utilizza per caricare event
        inferire il fotogramma. Una volta ottenuti i risultati, estrarrà le etichette event le coordinate (insieme ai punteggi)
        per ogni oggetto rilevato nel fotogramma.
        """
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        model.to(device)
        frame = [torch.tensor(frame)]
        results = self.model(frame)
        labels = results.xyxyn[0][:, -1].numpy()
        cord = results.xyxyn[0][:, :-1].numpy()
        return labels, cord

    def plot_boxes(self, results, frame):
        """
            The function below takes the results and the frame as input and plots boxes over all the objects which have a score higer than our threshold.
        """
        labels, cord = results
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        for i in range(n):
            row = cord[i]
            # If score is less than 0.2 we avoid making a prediction.
            if row[4] < 0.2:
                continue
            x1 = int(row[0] * x_shape)
            y1 = int(row[1] * y_shape)
            x2 = int(row[2] * x_shape)
            y2 = int(row[3] * y_shape)
            bgr = (0, 255, 0)  # color of the box
            classes = self.model.names  # Get the name of label index
            label_font = cv2.FONT_HERSHEY_SIMPLEX  # Font for the label.
            cv2.rectangle(frame, \
                          (x1, y1), (x2, y2), \
                          bgr, 2)  # Plot the boxes
            cv2.putText(frame, \
                        classes[labels[i]], \
                        (x1, y1), \
                        label_font, 0.9, bgr, 2)  # Put a label over box.
            return frame
