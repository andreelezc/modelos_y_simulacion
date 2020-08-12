from PyQt5.QtCore import *


class ModeloVacioCorrida(QAbstractTableModel):
    def __init__(self):
        super(ModeloVacioCorrida, self).__init__()
        self.headers = ['Semilla', 'Tasa de llegadas', 'Tasa de servicio', 'Usuarios iniciales']

    def rowCount(self, parent=None, *args, **kwargs):
        return 0

    def columnCount(self, parent=None, *args, **kwargs):
        return 4

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
            return super(ModeloVacioCorrida, self).headerData(column, orientation, role)

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable
