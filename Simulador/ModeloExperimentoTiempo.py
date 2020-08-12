from PyQt5.QtCore import *


class ModeloExperimentoTiempo(QAbstractTableModel):
    def __init__(self, simulacion):
        super(ModeloExperimentoTiempo, self).__init__()
        self.simulacion = simulacion
        self.headers = ['Cantidad de Servidores', 'Duracion en Horas']

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.simulacion.experimentos)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.headers)

    def update(self):
        self.layoutChanged.emit()

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            i = index.row()
            j = index.column()
            exp = self.simulacion.experimentos[i]
            if j == 0:
                return exp.num_serv
            elif j == 1:
                return exp.duracion/60
        else:
            return QVariant()

    def headerData(self, column, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[column]
        else:
            return super(ModeloExperimentoTiempo, self).headerData(column, orientation, role)

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def agregar_exp(self, horas, servidores):
        self.simulacion.crear_exp(horas, servidores)
        self.layoutChanged.emit()

    def eliminar_exp(self, indice):
        del self.simulacion.experimentos[indice]
        self.layoutChanged.emit()

    def editar_exp(self, indice, servidores, duracion):
        exp = self.simulacion.experimentos[indice]
        exp.num_serv = servidores
        exp.duracion = duracion
        self.layoutChanged.emit()
