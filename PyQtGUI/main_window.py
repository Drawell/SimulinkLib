import os.path
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QDockWidget, QAction, QFileDialog
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQtGUI import SimElementListModel, SimElementListView, ViewWidget
from Environment import Environment, EnvManager


class GeneralWindow(QMainWindow):
    def __init__(self):
        super(GeneralWindow, self).__init__(None)
        self.environment = Environment(0, 0, 500, 500, 'MainEnvironment')
        self.env_manager = EnvManager(self.environment)
        self.init_component()
        self.show()

    def init_component(self):
        self.setWindowTitle("PySimulink")

        self.main_layout = QHBoxLayout(self)
        self.setCentralWidget(QWidget(self))
        self.centralWidget().setLayout(self.main_layout)

        self.view_widget = ViewWidget(self, self.env_manager)
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
        file_menu.addAction(show_el_action)

        save_action = QAction('Save to xml', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_to_xml)
        file_menu.addAction(save_action)

        open_action = QAction('Open xml', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_xml)
        file_menu.addAction(open_action)

        tools_menu = self.menuBar().addMenu('tools')
        tools_menu.addAction(show_el_action)

        run_action = QAction(QIcon(os.path.join(os.path.dirname(__file__), 'Resources', 'run.png')), 'Run', self)
        self.tool_bar = self.addToolBar('tool_bar')
        self.tool_bar.addAction(run_action)

        self.sim_elem_dock = QDockWidget('Elements', self)
        self.sim_elem_dock.setMaximumWidth(150)
        self.sim_elem_dock.setMinimumWidth(100)

        list_view = SimElementListView(self.sim_elem_dock)
        self.class_model = SimElementListModel(self.sim_elem_dock)
        list_view.setModel(self.class_model)

        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'SimStandardElements')
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

        self.env_manager.add_element_by_name(name, x, y)
        self.view_widget.update()
        self.update()

    @pyqtSlot(name='save_to_xml')
    def save_to_xml(self):
        path = QFileDialog.getSaveFileName(self, 'Save file',
                                           os.path.dirname(os.path.dirname(__file__)), "XML Files (*.xml)")[0]

        if path and path != '':
            self.env_manager.save_to_xml(path)

    @pyqtSlot(name='open_xml')
    def open_xml(self):
        path = QFileDialog.getOpenFileName(self, 'Open file',
                                           os.path.dirname(os.path.dirname(__file__)), "XML Files (*.xml)")[0]

        if path and path != '':
            self.env_manager.parse_xml(path)
            self.update()

    @pyqtSlot(name='start_simulation')
    def start_simulation(self):
        pass