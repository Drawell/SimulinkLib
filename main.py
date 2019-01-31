import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from main_window import GeneralWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GeneralWindow()
    sys.exit(app.exec_())
