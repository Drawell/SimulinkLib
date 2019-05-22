from PyQt5.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal


class ContextWidget(QDialog):
    var_changed_signal = pyqtSignal(str, float)
    refresh_signal = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("Variables")
        self.global_layout = QVBoxLayout(self)
        self.main_layout = QVBoxLayout(self)
        self.refresh_btn = QPushButton('Refresh', self)
        self.refresh_btn.clicked.connect(lambda: self.refresh_signal.emit())

        self.global_layout.addWidget(self.refresh_btn, alignment=Qt.AlignAbsolute)
        self.global_layout.addLayout(self.main_layout)
        self.global_layout.addStretch()
        self.setLayout(self.global_layout)

    def refresh(self, context):
        self.clear_layout()

        for key, value in context.items():
            tmp_layout = QHBoxLayout(self)
            label = QLabel(key, self)
            text_edit = QLineEdit(str(value), self)
            text_edit.textChanged.connect(lambda value, variable=key: self.change_value(variable, value))
            tmp_layout.addWidget(label, alignment=Qt.AlignAbsolute)
            tmp_layout.addWidget(text_edit, alignment=Qt.AlignAbsolute)
            self.main_layout.addLayout(tmp_layout)

    def change_value(self, variable, value):
        try:
            value = float(value)
        except:
            value = value[:1]
        self.var_changed_signal.emit(variable, float(value))

    def clear_layout(self):
        while self.main_layout.count() > 0:
            l = self.main_layout.itemAt(0).layout()

            # label
            i = l.itemAt(0).widget()
            l.itemAt(0).widget().setParent(None)
            i.deleteLater()

            # text edit
            i = l.itemAt(0).widget()
            l.itemAt(0).widget().setParent(None)
            i.deleteLater()

            self.main_layout.itemAt(0).layout().setParent(None)
            l.deleteLater()
