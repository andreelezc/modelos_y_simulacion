from GUIs.about_ui import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QDesktopWidget, QApplication


class About(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, *args, **kwargs):
        QtWidgets.QDialog.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.center()
        self.setFixedSize(400, 300)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        self.bAceptar.clicked.connect(self.click_aceptar)

    def center(self):
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())

    def click_aceptar(self):
        self.close()
