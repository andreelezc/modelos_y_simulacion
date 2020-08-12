from PyQt5.QtCore import *


class ModeloCalcSimulacion(QAbstractTableModel):
    def __init__(self, calculo_simulacion):
        super(ModeloCalcSimulacion, self).__init__()
        self.calc_simulacion = calculo_simulacion
        self.headers = ['Experimento Nº', 'Media de Llegadas', 'Media de Atención',
                        'Media de Permanencia']

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.calc_simulacion.calc_exp)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.headers)

    def update(self):
        self.layoutChanged.emit()

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            i = index.row()
            j = index.column()
            calculo_exp = self.calc_simulacion.calc_exp[i]
            datos = [i + 1, '{:.2f}'.format(calculo_exp.media_lleg), '{:.2f}'.format(calculo_exp.media_atencion),
                     '{:.2f}'.format(calculo_exp.media_perm)]
            return datos[j]
        else:
            return QVariant()

    def headerData(self, column, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[column]
        else:
            return super(ModeloCalcSimulacion, self).headerData(column, orientation, role)

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable
