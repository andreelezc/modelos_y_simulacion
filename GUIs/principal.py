from GUIs.principal_ui import Ui_MainWindow
from GUIs import datostiempo, datoscantidad, about
import Simulador.DatosPrincipal
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDesktopWidget


class Principal(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        self.ventanaDatos = None
        self.ventanaAbout = None
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.center()

        # Crea grupo de botones
        self.group = QtWidgets.QButtonGroup()
        self.group.addButton(self.colaTiempo)
        self.group.addButton(self.colaCant)

        self.config_validacion()

        # Conectar validacion de colores
        self.sistemaLineEdit.textChanged.connect(self.check_state)
        self.servidorLineEdit.textChanged.connect(self.check_state)
        self.usuarioLineEdit.textChanged.connect(self.check_state)

        self.colaTiempo.toggled.connect(self.habilitar_boton)
        self.colaCant.toggled.connect(self.habilitar_boton)

        # Conectar el click de Limpiar
        self.bLimpiar.clicked.connect(self.click_limpiar)

        # Conectar el click de Siguiente con la accion
        self.bSiguiente.clicked.connect(self.click_siguiente)

        # Conectar el click de About con la accion
        self.bAcercaDe.clicked.connect(self.click_about)

    def center(self):
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())

    def click_siguiente(self):
        datos = Simulador.DatosPrincipal.DatosPrincipal(self.sistemaLineEdit.text(), self.servidorLineEdit.text(), self.usuarioLineEdit.text())
        if self.colaTiempo.isChecked():
            self.ventanaDatos = datostiempo.DatosTiempo(self, datos)
            if self.isMaximized():
                self.ventanaDatos.showMaximized()
            else:
                self.ventanaDatos.show()
        elif self.colaCant.isChecked():
            self.ventanaDatos = datoscantidad.DatosCantidad(self, datos)
            if self.isMaximized():
                self.ventanaDatos.showMaximized()
            else:
                self.ventanaDatos.show()
            self.ventanaDatos.show()
        self.hide()

    def click_limpiar(self):
        """Limpia todos los campos"""
        self.group.setExclusive(False)
        self.colaTiempo.setChecked(False)
        self.colaCant.setChecked(False)
        self.group.setExclusive(True)
        self.sistemaLineEdit.clear()
        self.sistemaLineEdit.setStyleSheet('QLineEdit { background-color: white }')
        self.servidorLineEdit.clear()
        self.servidorLineEdit.setStyleSheet('QLineEdit { background-color: white }')
        self.usuarioLineEdit.clear()
        self.usuarioLineEdit.setStyleSheet('QLineEdit { background-color: white }')

    def config_validacion(self):
        regexp = QtCore.QRegExp('.*\\S.*')  # Permite cualquier caracter excepto lineas en blanco
        validator = QtGui.QRegExpValidator(regexp)
        self.sistemaLineEdit.setValidator(validator)
        self.servidorLineEdit.setValidator(validator)
        self.usuarioLineEdit.setValidator(validator)

    def check_state(self):
        sender = self.sender()
        validator = sender.validator()
        state = validator.validate(sender.text(), 0)[0]
        if state == QtGui.QValidator.Acceptable:
            color = '#c4df9b'  # green
        elif state == QtGui.QValidator.Intermediate:
            color = '#f6989d'  # red (#fff79a yellow)
        else:
            color = '#f6989d'  # red
        sender.setStyleSheet('QLineEdit { background-color: %s; font-size: 11pt }' % color)

        self.habilitar_boton()

    def habilitar_boton(self):
        if (self.colaTiempo.isChecked() or self.colaCant.isChecked()) \
                and (self.sistemaLineEdit.text()
                     and self.servidorLineEdit.text()
                     and self.usuarioLineEdit.text()):
            self.bSiguiente.setEnabled(True)
        else:
            self.bSiguiente.setEnabled(False)

    def click_about(self):
        self.ventanaAbout = about.About()
        self.ventanaAbout.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    app.setStyle('fusion')
    window = Principal()
    window.show()
    app.exec_()
