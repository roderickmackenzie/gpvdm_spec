import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import *
from planet import *


class checkBoxInput(QWidget):
    def __init__(self, parentObject, parent=None):
        super(checkBoxInput, self).__init__(parent)
        self.resize(100,200)
        self.parentObject = parentObject

        layout = QVBoxLayout()
        self.b1 = QCheckBox("Title")
        self.b1.setChecked(self.parentObject.states[0])
        layout.addWidget(self.b1)

        self.b2 = QCheckBox("BlackBody")
        self.b2.setChecked(self.parentObject.states[1])
        layout.addWidget(self.b2)

        self.b3 = QCheckBox("Extraterrestrial")
        self.b3.setChecked(self.parentObject.states[2])
        layout.addWidget(self.b3)

        self.b4 = QCheckBox("Direct")
        self.b4.setChecked(self.parentObject.states[3])
        if parentObject.enable_earthattr:
            layout.addWidget(self.b4)

        self.b5 = QCheckBox("Diffuse")
        self.b5.setChecked(self.parentObject.states[4])
        self.b5.stateChanged.connect(lambda: self.b5)
        if parentObject.enable_earthattr:
            layout.addWidget(self.b5)

        self.b6 = QCheckBox("Total")
        self.b6.setChecked(self.parentObject.states[5])
        if parentObject.enable_earthattr:
            layout.addWidget(self.b6)
        if parentObject.enable_marsattr:
            layout.addWidget(self.b6)
        if parentObject.enable_venusattr:
            layout.addWidget(self.b6)

        self.b7 = QCheckBox("Legend")
        self.b7.setChecked(self.parentObject.states[6])
        layout.addWidget(self.b7)

        self.okButton = QPushButton('Apply')
        layout.addWidget(self.okButton)
        self.okButton.clicked.connect(self.getPreferences)


        self.setLayout(layout)
        self.center()

    def getPreferences(self):
        TitleState = self.b1.isChecked()
        BlackBodyState = self.b2.isChecked()
        ETState = self.b3.isChecked()
        DirectState = self.b4.isChecked()
        DiffuseState = self.b5.isChecked()
        TotalState = self.b6.isChecked()
        LegendState = self.b7.isChecked()
        self.parentObject.states = [TitleState, BlackBodyState, ETState, DirectState, DiffuseState, TotalState, LegendState]
        self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

