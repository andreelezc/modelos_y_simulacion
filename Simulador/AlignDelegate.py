from PyQt5 import QtCore, QtWidgets


class AlignDelegate(QtWidgets.QItemDelegate):
    def paint(self, painter, option, index):
        option.displayAlignment = QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
        QtWidgets.QItemDelegate.paint(self, painter, option, index)
