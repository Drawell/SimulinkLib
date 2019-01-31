import sys
import os.path
from PyQt5.QtWidgets import * #QMainWindow, QWidget, QHBoxLayout, QDockWidget, QMenuBar, QAction, QListView
from PyQt5.QtCore import Qt, pyqtSlot
from sim_element_list import SimElementListModel, SimElementListView
from view_widget import ViewWidget
from environment import Environment
from env_manager import EnvManager


class GeneralWindow(QMainWindow):
    def __init__(self):
        super(GeneralWindow, self).__init__(None)
        self.environment = Environment()
        self.env_manager = EnvManager(self.environment)
        self.init_component()
        self.show()

    def init_component(self):
        self.setWindowTitle("PySimulink")

        self.main_layout = QHBoxLayout(self)
        self.setCentralWidget(QWidget(self))
        self.centralWidget().setLayout(self.main_layout)

        self.view_widget = ViewWidget(self)
        self.view_widget.add_element_signal.connect(self.add_element_by_name)

        self.main_layout.addWidget(self.view_widget)
        file_menu = self.menuBar().addMenu('file')

        quit_action = QAction('Quit', self)
        quit_action.setShortcut('Ctrl+Q')
        quit_action.triggered.connect(self.close)

        file_menu.addAction(quit_action)

        import_el_action = QAction('Import', self)
        import_el_action.triggered.connect(self.import_elements)

        file_menu.addAction(import_el_action)

        show_el_action = QAction('Elements', self)
        show_el_action.setShortcut('Ctrl+E')
        show_el_action.triggered.connect(self.show_sim_elem_dock)

        tools_menu = self.menuBar().addMenu('tools')
        tools_menu.addAction(show_el_action)

        self.sim_elem_dock = QDockWidget('Elements', self)
        self.sim_elem_dock.setMaximumWidth(150)
        self.sim_elem_dock.setMinimumWidth(100)

        list_view = SimElementListView(self.sim_elem_dock)
        self.class_model = SimElementListModel(self.sim_elem_dock)
        list_view.setModel(self.class_model)

        path = os.path.join(os.path.dirname(__file__), 'SimStandardModules')
        self.env_manager.import_classes_from_dir(path)
        self.class_model.setData(0, self.env_manager.imported_classes)

        self.sim_elem_dock.setWidget(list_view)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.sim_elem_dock)

    def show_sim_elem_dock(self):
        self.sim_elem_dock.show()

    @pyqtSlot(name='import_elements')
    def import_elements(self):
        '''
        подгружает новые классы из папки
        :return: ничего
        '''
        dir_path = QFileDialog.getExistingDirectory(self, 'Open directory with elements',
                                                    os.path.dirname(__file__), QFileDialog.ShowDirsOnly)
        if dir_path and dir_path != '':
            self.env_manager.import_classes_from_dir(dir_path)
            self.class_model.setData(0, self.env_manager.imported_classes)
            self.update()

    @pyqtSlot(str, int, int, name='add_element_by_name')
    def add_element_by_name(self, name: str, x: int, y: int):
        '''
        Добавляет элемент в среду по имени с помощью менеджера и перерисовывает
        :param name: имя класса
        :param x: координата x на view_widget
        :param y: координата y на view_widget
        :return: ничего
        '''

        self.env_manager.add_class_by_name(name, x, y)
        self.view_widget.draw_pixmap(self.environment.draw_qpixmap())
        self.update()
