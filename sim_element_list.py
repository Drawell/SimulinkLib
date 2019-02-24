from PyQt5.QtWidgets import QWidget, QFrame, QListView, QAbstractItemView
from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QVariant, QMimeData, QByteArray, QDataStream, QIODevice, QSize
from PyQt5.QtGui import QPixmap, QDrag, QMouseEvent, QDragMoveEvent, QDragLeaveEvent, QDragEnterEvent, QImage
from typing import List, Dict, Union
from sim_base_class import SimBaseClass
#from SimStandardModules.SimScope import *

## @package sim_element_list
#  Описывает виджет для просмотра, модель данных и элемент этих самых данных
#
#


## Элемент, который хронит класс
#
# Не хранит в себе еще и картинку, с некоторым масштабом, что бы они были одинаковыми
class SimElementItem(QFrame):
    def __init__(self, parent, sim_element_type: SimBaseClass):
        super(SimElementItem, self).__init__(parent)
        self.element_type = sim_element_type
        #self.pixmap = QPixmap(self.element_type.get_img_path()).scaled(50, 50)
        self.pixmap = QPixmap(QImage.fromData(self.element_type.get_base_img_as_byte_data(50, 50)))

    def __str__(self):
        return 'sim_item: ' + self.element_type.get_name()

    def get_img(self)->str:
        return self.pixmap

    def get_name(self)->str:
        return self.element_type.get_name()

## Простой список с элементами
#
# Data, в зависимости от роли, возвращает картинку, имя, которое класс возвращает через статическую функцию,
# или имя класса, оно передается через DragDrop и используется для нахождения нужного класса в словаре менеджера среды
class SimElementListModel(QAbstractListModel):
    def __init__(self, parent):
        super(SimElementListModel, self).__init__(parent)
        self.parent_wid = parent
        self.data_list = []

    def rowCount(self, parent=QModelIndex())->int:
        return len(self.data_list)

    def data(self, index: QModelIndex, role: int)->QVariant:
        if index.isValid():
            if role == Qt.DisplayRole:
                return QVariant(self.data_list[index.row()].get_name())
            if role == Qt.DecorationRole:
                pixmap = self.data_list[index.row()].get_img()
                return QVariant(pixmap)
            if role == Qt.UserRole:
                return QVariant(self.data_list[index.row()].element_type.__name__)
        return QVariant()

    def setData(self, index, value, role=0):  # dict_of_element_classes):
        self.data_list = []
        self.beginInsertRows(QModelIndex(), 0, len(value) - 1)
        for i, item in enumerate(value.values()):
            self.data_list.append(SimElementItem(self.parent_wid, item))
            index = self.createIndex(i, 0, None)
            self.dataChanged.emit(index, index)
        self.endInsertRows()

## Виджет с моделью
#
# Ничего интересного, только магия с DragDrop
class SimElementListView(QListView):
    def __int__(self, parent: QWidget):
        super(SimElementListView, self).__init__(parent)
        self.setIconSize(QSize(50, 50))
        self.setDragEnabled(True)
        self.setAcceptDrops(False)
        self.setDropIndicatorShown(True)
        self.setSelectionMode(QAbstractItemView.SingleSelection)

    def mousePressEvent(self, event: QMouseEvent):
        index = self.indexAt(event.pos())
        class_name = self.model().data(index, Qt.UserRole).value()
        pixmap = self.model().data(index, Qt.DecorationRole).value()

        item_data = QByteArray()
        data_stream = QDataStream(item_data, QIODevice.WriteOnly)
        data_stream.writeQString(class_name)

        mime_data = QMimeData()
        mime_data.setData("application/x-simitemdata", item_data)

        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setPixmap(pixmap)
        drag.exec(Qt.MoveAction)

    def dragLeaveEvent(self, event: QDragLeaveEvent):
        event.accept()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasFormat("application/x-simitemdata"):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent):
        if event.mimeData().hasFormat("application/x-simitemdata"):
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()
