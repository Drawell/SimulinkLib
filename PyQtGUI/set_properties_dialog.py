from PyQt5.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt

from PySimCore import SimBaseClass


class SetPropertiesDialog(QDialog):
    def __init__(self, parent, element: SimBaseClass):
        super().__init__(parent)
        self.element = element

        self.setWindowTitle(element.properties['name'])
        self.main_layout = QVBoxLayout(self)
        self.layout().addLayout(self.main_layout)
        self.text_edits = {}

        for key, value in element.properties.items():
            if key in ['x', 'y', 'width', 'height', 'name']:
                continue

            tmp_layout = QHBoxLayout(self)
            label = QLabel(key, self)
            text_edit = QLineEdit(str(value), self)
            tmp_layout.addWidget(label, alignment=Qt.AlignAbsolute)
            tmp_layout.addWidget(text_edit, alignment=Qt.AlignAbsolute)
            self.main_layout.addLayout(tmp_layout)

            self.text_edits[key] = text_edit

        tmp_layout = QHBoxLayout(self)

        btn_cancel = QPushButton('Cancel', self)
        btn_cancel.clicked.connect(self.close)
        tmp_layout.addWidget(btn_cancel, alignment=Qt.AlignRight)

        btn_ok = QPushButton('Ok', self)
        btn_ok.clicked.connect(self.__set_ok__)
        btn_ok.setFocus(True)
        tmp_layout.addWidget(btn_ok, alignment=Qt.AlignRight)

        self.main_layout.addLayout(tmp_layout)

    def __set_ok__(self):
        self.ok = True
        new_properties = {}
        for key, value in self.text_edits.items():
            new_properties[key] = value.text()

        self.element.update(new_properties)
        self.close()
