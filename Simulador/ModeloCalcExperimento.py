from PyQt5.QtCore import *


class ModeloCalcExperimento(QAbstractTableModel):
    def __init__(self, calc_experimento):
        super(ModeloCalcExperimento, self).__init__()
        self.calc_experimento = calc_experimento
        self.headers = ['Corrida Nº', 'Media de Llegada', 'Media de Espera', 'Media de Permanencia',
                        'Long. Media de Cola', 'Porc. de Utilización', 'Porc. de Ocio']

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.calc_experimento.calc_corr)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.headers)

    def update(self):
        self.layoutChanged.emit()

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            i = index.row()
            j = index.column()
            calculo_corrida = self.calc_experimento.calc_corr[i]
            datos = [i + 1, '{:.2f}'.format(calculo_corrida.media_lleg), '{:.2f}'.format(calculo_corrida.media_espera),
                     '{:.2f}'.format(calculo_corrida.media_perm), '{:.2f}'.format(calculo_corrida.long_prom_cola),
                     '{:.2f}'.format(calculo_corrida.utilizacion), '{:.2f}'.format(calculo_corrida.ocio)]
            return datos[j]
        else:
            return QVariant()

    def headerData(self, column, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[column]
        else:
            return super(ModeloCalcExperimento, self).headerData(column, orientation, role)

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable
