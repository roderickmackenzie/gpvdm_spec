import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import os

from planet import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(1200,600)


        exitAction = QAction(QIcon(os.path.join(os.getcwd(), 'icons', 'exit.png')), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        saveFigureAction =  QAction(QIcon(os.path.join(os.getcwd(), 'icons', 'save.png')), 'Save Figure', self)
        saveFigureAction.setShortcut('Ctrl+S')
        saveFigureAction.triggered.connect(self.save)

        copyFigureAction =  QAction(QIcon(os.path.join(os.getcwd(), 'icons', 'copy.png')), 'Copy Figure', self)
        copyFigureAction.setShortcut('Ctrl+C')
        copyFigureAction.triggered.connect(self.copy)

        # plotPreferencesAction =  QAction(QIcon(os.path.join(os.getcwd(), 'icons', 'prefs.png')), 'Plot Preferences', self)
        # plotPreferencesAction.triggered.connect(self.setPlotPreferences)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(saveFigureAction)
        fileMenu.addAction(copyFigureAction)

        # optionsMenu = menubar.addMenu('&Options')
        # optionsMenu.addAction(plotPreferencesAction)

        self.setWindowTitle('Solar Spectrum Planetary Model')
        self.center()
        self.show()

        self.tabs = QTabWidget()

        self.setCentralWidget(self.tabs)

        earth = planet()
        earth.set_earth(True)
        earth.init()
        self.tabs.addTab(earth,"Earth")

        mercury = planet()
        mercury.set_mercury(True)
        mercury.set_orbitalpoint(True)
        mercury.init()
        self.tabs.addTab(mercury,"Mercury")

        venus = planet()
        venus.set_venus(True)
        venus.set_orbitalpoint(True)
        venus.init()
        self.tabs.addTab(venus,"Venus")

        mars = planet()
        mars.set_mars(True)
        mars.set_orbitalpoint(True)
        mars.init()
        self.tabs.addTab(mars,"Mars")

        ceres = planet()
        ceres.set_ceres(True)
        ceres.set_orbitalpoint(True)
        ceres.init()
        self.tabs.addTab(ceres, "Ceres (Dwarf Planet)")

        europa = planet()
        europa.set_europa(True)
        europa.set_orbitalpoint(True)
        europa.init()
        self.tabs.addTab(europa, "Europa (moon of Jupiter)")

        halley = planet()
        halley.set_halley(True)
        halley.set_orbitalpoint(True)
        halley.init()
        self.tabs.addTab(halley, "Halley's Comet")

        pluto = planet()
        pluto.set_pluto(True)
        pluto.set_orbitalpoint(True)
        pluto.init()
        self.tabs.addTab(pluto, "Pluto")


    # def setPlotPreferences(self):
    #     self.tabs.currentWidget().setPlotPreferences()

    def save(self):
        self.tabs.currentWidget().save()

    def copy(self):
        self.tabs.currentWidget().copy2clip()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())