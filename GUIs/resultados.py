from GUIs.resultados_ui import Ui_MainWindow
from GUIs import principal
from PyQt5.QtWidgets import QDesktopWidget, QScrollArea
from Simulador.TreeModel import *
from Simulador.CalculosSimulacion import *
from Simulador.ModeloCalcCorrida import *
from Simulador.ModeloCalcExperimento import *
from Simulador.ModeloCalcSimulacion import *
from Simulador.AlignDelegate import *
import xlsxwriter
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from Simulador.GraficosSimulacion import *
import os
from io import BytesIO


class Resultados(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, simulacion, datos, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.simulacion = simulacion
        self.datos = datos
        self.ventanaPrincipal = None
        self.setupUi(self)
        self.center()

        # a figure instance to plot on
        self.figure = Figure(tight_layout=True, figsize=(10, 5))
        self.imgdata = BytesIO()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        self.scroll = QScrollArea(self)
        self.scroll.setWidget(self.canvas)

        # set the layout
        self.layoutGrafico.addWidget(self.scroll)

        # Crear calculos
        self.calculo_sim = CalculosSimulacion(self.simulacion)
        self.calculo_sim.calcular_sim()

        self.modeloarbol = TreeModel(self.calculo_sim)
        self.treeView.setModel(self.modeloarbol)
        self.treeView.setHeaderHidden(True)
        self.treeView.expandAll()

        # Conectar el click de Finalizar con la accion
        self.bFinalizar.clicked.connect(self.click_finalizar)

        # Conectar el click de Volver con la accion
        self.bVolver.clicked.connect(self.click_menu_princ)

        # Conectar el click en el arbol para cargar tabla resultados
        self.treeView.clicked.connect(self.cargar_resultados)

        # Conectar el click en exportar con la accion
        self.bExportar.clicked.connect(self.click_exportar)

    def changeEvent(self, event, *args, **kwargs):
        if event.type() == QEvent.WindowStateChange:
            if self.tablaResultados.model() is not None:
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

    def cargar_resultados(self, indice):
        elemento = indice.internalPointer().elemento
        modelo = None

        if isinstance(elemento, CalculosCorrida):
            self.figure.clf()
            modelo = ModeloCalcCorrida(elemento)
            modelo.headers[0] = self.datos.usuario + ' Nº'
            modelo.headers[8] = self.datos.servidor + ' Nº'
            g_c = GraficosCorrida(elemento, self.figure)
            g_c.graficar_corrida()
            self.canvas.draw()

        elif isinstance(elemento, CalculosExperimento):
            self.figure.clf()
            modelo = ModeloCalcExperimento(elemento)
            g_e = GraficosExp(elemento, self.figure)
            g_e.graficar_exp()
            self.canvas.draw()

        elif isinstance(elemento, CalculosSimulacion):
            self.figure.clf()
            modelo = ModeloCalcSimulacion(elemento)
            g_s = GraficarSim(elemento, self.figure)
            g_s.graficar_sim()
            self.canvas.draw()

        self.tablaResultados.setModel(modelo)
        self.tablaResultados.setItemDelegate(AlignDelegate())
        self.maximizar_headers()

    def maximizar_headers(self):
        header = self.tablaResultados.horizontalHeader()
        if self.isMaximized():
            for i in range(self.tablaResultados.model().columnCount()):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
        else:
            for i in range(self.tablaResultados.model().columnCount()):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

    def click_menu_princ(self):
        self.ventanaPrincipal = principal.Principal()
        self.ventanaPrincipal.show()
        self.hide()

    def click_exportar(self):
        name = 'resultados ' + self.datos.sistema
        name = name.replace(' ', '_').lower()
        options = QtWidgets.QFileDialog.Options()
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self.tablaResultados, 'Exportar Resultados', name, ".xlsx(*.xlsx)", options=options)
        if not filename:
            return
        workbook = xlsxwriter.Workbook(filename)
        sheet1 = workbook.add_worksheet("Resultados")
        sheet2 = workbook.add_worksheet("Gráficos")
        self.add2(sheet1, sheet2, workbook)
        workbook.close()
        os.system('start ' + filename)

    def add2(self, sheet1, sheet2, workbook):
        # Guardar tabla de resultados
        parent = QModelIndex()
        headers = self.tablaResultados.model().headers
        cell_format = workbook.add_format({'bold': True})
        cell_format.set_align('center')
        cell_format2 = workbook.add_format()
        cell_format2.set_align('right')
        for i in range(len(headers)):
            sheet1.write(0, i, headers[i], cell_format)
        for row in range(self.tablaResultados.model().rowCount()):
            for column in range(self.tablaResultados.model().columnCount()):
                index = self.tablaResultados.model().index(row, column, parent)
                sheet1.write(row + 1, column, index.data(), cell_format2)
                sheet1.set_column(column, column, 20)
        # Guardar gráficos
        self.figure.savefig(self.imgdata, format="png")
        self.imgdata.seek(0)
        sheet2.insert_image(0, 0, "", {'image_data': self.imgdata})

    def click_finalizar(self):
        self.close()
