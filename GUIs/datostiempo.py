from GUIs.datostiempo_ui import Ui_MainWindow
from GUIs import resultados
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5 import QtGui
from Simulador.ModeloExperimentoTiempo import *
from Simulador.ModeloCorrida import *
from Simulador.ModeloVacioCorrida import *
from Simulador.SimulacionTiempo import *
from Simulador.AlignDelegate import *


class DatosTiempo(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, ventana, datos, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.ventanaResultados = None
        self.ventanaPrincipal = ventana
        self.datos = datos
        self.experimento_act = None
        self.setupUi(self)
        self.center()
        self.config_validacion()

        self.sim = Simulacion()

        # Asignar modelo de datos a TableView de Experimentos
        self.modelo_exp = ModeloExperimentoTiempo(self.sim)
        self.tablaExp.setModel(self.modelo_exp)

        self.tablaExp.setItemDelegate(AlignDelegate())
        header = self.tablaExp.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        # Asignar modelo de datos a TableView de Corridas
        self.modelo_corr_vacio = ModeloVacioCorrida()
        self.tablaCorridas.setModel(self.modelo_corr_vacio)
        self.maximizar_headers()

        # Conectar el click de Simular con la accion
        self.bSimular.clicked.connect(self.click_simular)

        # Conectar el click de AñadirExp con la accion
        self.bAnadirExp.clicked.connect(self.click_anadir_exp)

        # Conectar el click de EditarExp con la accion
        self.bEditarExp.clicked.connect(self.click_editar_exp)

        # Conectar el click de OkExp con la accion
        self.bOkEditarExp.clicked.connect(self.click_ok_exp)

        # Conectar el click de eliminar experimento
        self.bEliminarExp.clicked.connect(self.click_eliminar_exp)

        # Conectar el click de AnadirCorrida con la accion
        self.bAnadirCorrida.clicked.connect(self.click_anadir_corr)

        # Conectar el click de EditarCorrida con la accion
        self.bEditarCorrida.clicked.connect(self.click_editar_corrida)

        # Conectar el click de OkCorr con la accion
        self.bOkEditarCorrida.clicked.connect(self.click_ok_corr)

        # Conectar el click de EliminarCorr con la accion
        self.bEliminarCorrida.clicked.connect(self.click_eliminar_corr)

        # Conectar el click de Volver con la accion
        self.bVolver.clicked.connect(self.click_volver)

        # Conectar validacion de colores
        self.lineSemilla.textChanged.connect(self.check_state)
        self.lineTasaLleg.textChanged.connect(self.check_state)
        self.lineTasaServ.textChanged.connect(self.check_state)

        # Conectar el click en la lista de experimentos con llenar corridas
        self.tablaExp.clicked.connect(self.cargar_corridas)

    def changeEvent(self, event, *args, **kwargs):
        if event.type() == QEvent.WindowStateChange:
            self.maximizar_headers()

    def center(self):
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())

    def config_validacion(self):
        validator = QtGui.QIntValidator()
        self.lineSemilla.setValidator(validator)
        self.lineTasaLleg.setValidator(validator)
        self.lineTasaServ.setValidator(validator)

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

    def click_anadir_exp(self):
        cantHoras = 1*60
        cantServ = 1
        self.modelo_exp.agregar_exp(cantHoras, cantServ)
        self.bAnadirExp.setEnabled(False)

    def click_editar_exp(self):
        if self.experimento_act is None:
            return

        self.groupBoxEditarExp.setEnabled(True)
        self.bOkEditarExp.setEnabled(True)

        duracion = self.experimento_act.duracion
        servidores = self.experimento_act.num_serv
        self.sbCantHoras.setValue(duracion/60)
        self.sbCantServ.setValue(servidores)

    def click_ok_exp(self):
        item = self.tablaExp.selectionModel().selectedRows()[0]
        servidores = self.sbCantServ.value()
        duracion = self.sbCantHoras.value()
        duracion = duracion * 60

        self.modelo_exp.editar_exp(item.row(), servidores, duracion)

        self.bOkEditarExp.setEnabled(False)
        self.groupBoxEditarExp.setEnabled(False)

    def click_eliminar_exp(self):
        filas = self.tablaExp.selectionModel().selectedRows()
        for fila in filas:
            self.modelo_exp.eliminar_exp(fila.row())
        self.experimento_act = None
        if self.modelo_exp.rowCount() == 0:
            self.bSimular.setEnabled(False)

    def cargar_corridas(self, indice):
        self.experimento_act = self.sim.experimentos[indice.row()]
        modelo_corr = ModeloCorrida(self.experimento_act)
        self.tablaCorridas.setModel(modelo_corr)
        self.tablaCorridas.setItemDelegate(AlignDelegate())
        self.maximizar_headers()

    def click_anadir_corr(self):
        if self.experimento_act is None:
            return

        semilla = 1
        tasa_lleg = 1
        tasa_serv = 1
        u_ini = 0
        self.tablaCorridas.model().agregar_corrida(semilla, tasa_lleg, tasa_serv, u_ini)
        self.bAnadirExp.setEnabled(True)
        self.bSimular.setEnabled(True)

    def click_editar_corrida(self):
        items = self.tablaCorridas.selectionModel().selectedRows()

        if not items:
            return

        self.groupBoxEditarCorrida.setEnabled(True)
        self.bOkEditarCorrida.setEnabled(True)

        corrida = self.experimento_act.corridas[items[0].row()]
        semilla = corrida.semilla
        tasa_lleg = corrida.tasa_lleg
        tasa_serv = corrida.tasa_serv
        u_ini = corrida.u_ini

        self.lineSemilla.setText(str(semilla))
        self.lineTasaLleg.setText(str(tasa_lleg))
        self.lineTasaServ.setText(str(tasa_serv))
        self.sbUsuariosIni.setValue(u_ini)

    def click_ok_corr(self):
        item = self.tablaCorridas.selectionModel().selectedRows()[0]

        semilla = int(self.lineSemilla.text())
        tasa_lleg = int(self.lineTasaLleg.text())
        tasa_serv = int(self.lineTasaServ.text())
        u_ini = int(self.sbUsuariosIni.value())

        self.tablaCorridas.model().editar_corrida(item.row(), semilla, tasa_lleg, tasa_serv, u_ini)

        self.bOkEditarCorrida.setEnabled(False)
        self.groupBoxEditarCorrida.setEnabled(False)

    def click_eliminar_corr(self):
        filas = self.tablaCorridas.selectionModel().selectedRows()
        for fila in filas:
            self.tablaCorridas.model().eliminar_corrida(fila.row())
        if self.tablaCorridas.model().rowCount() == 0:
            self.bSimular.setEnabled(False)

    def habilitar_boton(self):
        if self.lineSemilla.text() and self.lineTasaLleg.text() and self.lineTasaServ.text():
            self.bSimular.setEnabled(True)
        else:
            self.bSimular.setEnabled(False)

    def maximizar_headers(self):
        header = self.tablaCorridas.horizontalHeader()
        if self.isMaximized():
            for i in range(self.tablaCorridas.model().columnCount()):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
        else:
            for i in range(self.tablaCorridas.model().columnCount()):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

    def click_simular(self):
        self.sim.ejecutar()
        self.ventanaResultados = resultados.Resultados(self.sim, self.datos)
        if self.isMaximized():
            self.ventanaResultados.showMaximized()
        else:
            self.ventanaResultados.show()
        self.hide()

    def click_volver(self):
        self.ventanaPrincipal.show()
        self.hide()

