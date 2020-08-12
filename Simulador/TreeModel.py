from PyQt5.QtCore import *
from Simulador.TreeItem import *


class TreeModel(QAbstractItemModel):
    def __init__(self, calc_simulacion):
        super(TreeModel, self).__init__()
        self.calc_simulacion = calc_simulacion

        self.headerItem = TreeItem(' ')
        self.rootItem = TreeItem('Simulacion', self.headerItem, self.calc_simulacion)
        self.headerItem.append_child(self.rootItem)
        self.setup_model_data()

    def columnCount(self, parent=None, *args, **kwargs):
        if parent.isValid():
            return parent.internalPointer().column_count()
        else:
            return self.headerItem.column_count()

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        if role != Qt.DisplayRole:
            return None

        item = index.internalPointer()

        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headerItem.data(section)

        return None

    def index(self, row, column, parent=None, *args, **kwargs):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.headerItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index=None):
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.headerItem:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent=None, *args, **kwargs):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.headerItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.child_count()

    def setup_model_data(self):
        for i in range(len(self.calc_simulacion.calc_exp)):
            exp = self.calc_simulacion.calc_exp[i]
            item = TreeItem('Experimento %d' % (i+1), self.rootItem, exp)
            self.rootItem.append_child(item)
            for j in range(len(exp.calc_corr)):
                item_c = TreeItem('Corrida %d' % (j+1), item, exp.calc_corr[j])
                item.append_child(item_c)
