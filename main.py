import sys
from PyQt5.QtWidgets import QApplication
from PyQtGUI.main_window import GeneralWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GeneralWindow()
    sys.exit(app.exec_())
