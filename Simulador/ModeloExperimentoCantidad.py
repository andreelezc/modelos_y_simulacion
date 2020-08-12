from PyQt5.QtCore import *


class ModeloExperimentoCantidad(QAbstractTableModel):
    def __init__(self, simulacion):
        super(ModeloExperimentoCantidad, self).__init__()
        self.simulacion = simulacion
        self.headers = ['Cantidad de Servidores', 'Cantidad de Usuarios']

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
                return exp.cantidad
        else:
            return QVariant()

    def headerData(self, column, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[column]
        else:
            return super(ModeloExperimentoCantidad, self).headerData(column, orientation, role)

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def agregar_exp(self, cantidad, servidores):
        self.simulacion.crear_exp(cantidad, servidores)
        self.layoutChanged.emit()

    def eliminar_exp(self, indice):
        del self.simulacion.experimentos[indice]
        self.layoutChanged.emit()

    def editar_exp(self, indice, servidores, cantidad):
        exp = self.simulacion.experimentos[indice]
        exp.num_serv = servidores
        exp.cantidad = cantidad
        self.layoutChanged.emit()
