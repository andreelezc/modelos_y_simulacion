class TreeItem(object):
    def __init__(self, data, parent=None, elemento=None):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []
        self.elemento = elemento

    def append_child(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def child_count(self):
        return len(self.childItems)

    def column_count(self):
        return 1

    def data(self, column):
        try:
            return self.itemData
        except IndexError:
            return None

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)

        return 0
