from PyQt5.QtCore import *


class ModeloCorrida(QAbstractTableModel):
    def __init__(self, experimento):
        super(ModeloCorrida, self).__init__()
        self.experimento = experimento
        self.headers = ['Semilla', 'Tasa de llegadas', 'Tasa de servicio', 'Usuarios iniciales']

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.experimento.corridas)

    def columnCount(self, parent=None, *args, **kwargs):
        return 4

    def update(self):
        self.layoutChanged.emit()

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            i = index.row()
            j = index.column()
            corrida = self.experimento.corridas[i]
            datos = [corrida.semilla, corrida.tasa_lleg, corrida.tasa_serv, corrida.u_ini]
            return datos[j]
        else:
            return QVariant()

    def headerData(self, column, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[column]
        else:
            return super(ModeloCorrida, self).headerData(column, orientation, role)

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def agregar_corrida(self, semilla, tasa_lleg, tasa_serv, u_ini):
        self.experimento.crear_corrida(semilla, tasa_lleg, tasa_serv, u_ini)
        self.layoutChanged.emit()

    def eliminar_corrida(self, indice):
        del self.experimento.corridas[indice]
        self.layoutChanged.emit()

    def editar_corrida(self, indice, semilla, tasa_lleg, tasa_serv, u_ini):
        corrida = self.experimento.corridas[indice]
        corrida.semilla = semilla
        corrida.tasa_lleg = tasa_lleg
        corrida.tasa_serv = tasa_serv
        corrida.u_ini = u_ini
        self.layoutChanged.emit()
