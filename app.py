import logging
import os
import sys

from PySide2.QtCore import Qt, QTimer, Signal
from PySide2.QtGui import QSurfaceFormat
from PySide2.QtQml import QQmlApplicationEngine, qmlRegisterType
from PySide2.QtWidgets import QApplication
import vtk

from src.graphics.engines import Fbo
from src.ctrls import MainCtrl
from src.utils import *

logging.basicConfig(filename="log.ini", level=logging.DEBUG)


def setVtkLog():
    logPath = os.path.join("log.ini")
    fow = vtk.vtkFileOutputWindow()
    fow.SetFileName(logPath)
    ow = vtk.vtkOutputWindow()
    ow.SetInstance(fow)


def registerCustomQml():
    qmlRegisterType(Fbo, "QmlVtk", 1, 0, "Fbo")


def compileQml():
    from src.utils import compileResourceFiles

    compileResourceFiles(rcDir="src/views", outDir="src/views")
    if os.path.isfile(os.path.join("src/views/rc_qml.py")):
        from src.views.rc_qml import qInitResources

        qInitResources()


class App(QApplication):
    def __init__(self, sys_argv):
        sys_argv += ["-style", "material"]  #! MUST HAVE
        super(App, self).__init__(sys_argv)
        self.engine = QQmlApplicationEngine()
        self.__mainCtrl = MainCtrl(self.engine)

    def setup(self):
        mainView = getQmlObject(self.engine, "MainView")
        if mainView.property("active"):
            self.__mainCtrl.setup()
        else:
            QTimer.singleShot(0, self.setup)


def main():
    registerCustomQml()
    compileQml()
    QSurfaceFormat.setDefaultFormat(setDefaultSurfaceFormat(False))

    app = App(sys.argv)

    if len(app.engine.rootObjects()) == 0:
        print("No QML file is loaded!")
        return

    #! Make sure MainView is active --> FboRenderer is created
    QTimer.singleShot(0, app.setup)
    sys.exit(app.exec_())


if __name__ == "__main__":
    setVtkLog()

    sys.excepthook = exceptHook

    main()
