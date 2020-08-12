from PyQt5.QtCore import *


class ModeloCalcCorrida(QAbstractTableModel):
    def __init__(self, calc_corrida):
        super(ModeloCalcCorrida, self).__init__()
        self.calc_corrida = calc_corrida
        self.headers = ['Usuario Nº', 'Llegada', 'Tiempo de Espera', 'Atención',
                        'Tiempo de Salida', 'Permanencia', 'Tiempo entre llegadas', 'En cola', 'Servidor']

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.calc_corrida.usuarios)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.headers)

    def update(self):
        self.layoutChanged.emit()

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            i = index.row()
            j = index.column()
            usuario = self.calc_corrida.usuarios[i]
            servidor = str(usuario.servidor + 1) if usuario.servidor is not None else '-'
            datos = [i+1, '{:.2f}'.format(usuario.llega), '{:.2f}'.format(usuario.espera), '{:.2f}'.format(usuario.atencion),
                     '{:.2f}'.format(usuario.deja), '{:.2f}'.format(usuario.permanencia), '{:.2f}'.format(self.calc_corrida.entre_llegadas[i]),
                     self.calc_corrida.cola[i], servidor]
            return datos[j]
        else:
            return QVariant()

    def headerData(self, column, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[column]
        else:
            return super(ModeloCalcCorrida, self).headerData(column, orientation, role)

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable
