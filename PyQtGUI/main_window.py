import os.path
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QDockWidget, QAction, QFileDialog, QLineEdit, QLabel,\
    QMessageBox
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQtGUI import SimElementListModel, SimElementListView, ViewWidget, ContextWidget
from PySimCore import Environment


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__(None)
        self.env = Environment()
        self.context = {}
        self.import_directories = []
        self.import_directories.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'SimStandardElements'))
        self.import_classes()
        self.init_component()
        self.show()


    def init_component(self):
        self.setWindowTitle("PySimulink")

        self.main_layout = QHBoxLayout(self)
        self.setCentralWidget(QWidget(self))
        self.centralWidget().setLayout(self.main_layout)

        self.view_widget = ViewWidget(self, self.env)
        #self.view_widget.add_element_signal.connect(self.add_element_by_name)

        self.main_layout.addWidget(self.view_widget)
        file_menu = self.menuBar().addMenu('file')

        # ****  MENU *****
        # ****  File *****
        quit_action = QAction('Quit', self)
        quit_action.setShortcut('Ctrl+Q')
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        import_el_action = QAction('Import', self)
        import_el_action.triggered.connect(self.import_elements)
        file_menu.addAction(import_el_action)

        save_action = QAction('Save to xml', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_to_xml)
        file_menu.addAction(save_action)

        open_action = QAction('Open xml', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_xml)
        file_menu.addAction(open_action)

        # **** View  *****
        view_menu = self.menuBar().addMenu('view')

        show_el_action = QAction('Elements', self)
        show_el_action.setShortcut('Ctrl+E')
        show_el_action.triggered.connect(self.show_sim_elem_dock)
        view_menu.addAction(show_el_action)

        show_context_action = QAction('Context', self)
        show_context_action.setShortcut('Ctrl+X')
        show_context_action.triggered.connect(self.show_context_dock)
        view_menu.addAction(show_context_action)

        view_menu.addAction(show_context_action)

        # ****  TOOL BAR *****
        self.tool_bar = self.addToolBar('tool_bar')

        run_action = QAction(QIcon(os.path.join(os.path.dirname(__file__), 'Resources', 'run.png')), 'Run', self)
        run_action.setShortcut('F5')
        run_action.triggered.connect(self.start_simulation)
        self.tool_bar.addAction(run_action)

        self.tool_bar.addWidget(QLabel('Start: '))
        self.start_time_line_edit = QLineEdit('0', self)
        self.start_time_line_edit.setMaximumWidth(40)
        self.tool_bar.addWidget(self.start_time_line_edit)

        self.tool_bar.addWidget(QLabel(' End: '))
        self.end_time_line_edit = QLineEdit('10', self)
        self.end_time_line_edit.setMaximumWidth(40)
        self.tool_bar.addWidget(self.end_time_line_edit)

        self.tool_bar.addWidget(QLabel(' Interval: '))
        self.interval_time_line_edit = QLineEdit('0.1', self)
        self.interval_time_line_edit.setMaximumWidth(40)
        self.tool_bar.addWidget(self.interval_time_line_edit)

        # ****  DOCKS *****

        self.sim_elem_dock = QDockWidget('Elements', self)
        self.sim_elem_dock.setMaximumWidth(200)
        self.sim_elem_dock.setMinimumWidth(100)

        list_view = SimElementListView(self.sim_elem_dock)
        self.class_model = SimElementListModel(self.sim_elem_dock)
        list_view.setModel(self.class_model)

        self.class_model.setData(0, self.env.imported_classes)

        self.sim_elem_dock.setWidget(list_view)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.sim_elem_dock)

        self.context_dock = QDockWidget('Context', self)
        self.context_dock.setMaximumWidth(200)
        self.context_dock.setMinimumWidth(100)
        self.context_widget = ContextWidget(self)
        self.context_widget.var_changed_signal.connect(self.context_value_changed)
        self.context_widget.refresh_signal.connect(self.refresh_context_widget)
        self.context_dock.setWidget(self.context_widget)
        self.context_dock.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea)

        self.addDockWidget(Qt.RightDockWidgetArea, self.context_dock)

    def import_classes(self):
        for dir in self.import_directories:
            try:
                self.env.import_classes_from_dir(dir)
            except Exception as e:
                msg = QMessageBox(self, )
                msg.setWindowTitle("Import Error")
                msg.setText(str(e.args[0]))
                msg.addButton(QMessageBox.Ok)
                msg.setDefaultButton(QMessageBox.Ok)
                msg.show()

    def update_context(self, update_widget: bool=True):
        for var in self.env.get_variable_list():
            if var not in self.context:
                self.context[var] = 0

        if update_widget:
            self.context_widget.refresh(self.context)

    @pyqtSlot(str, float, name='context_value_changed')
    def context_value_changed(self, variable: str, value: float):
        self.context[variable] = value

    @pyqtSlot(name='refresh_context_widget')
    def refresh_context_widget(self):
        self.update_context()

    @pyqtSlot(name='show_sim_elem_dock')
    def show_sim_elem_dock(self):
        self.sim_elem_dock.show()

    @pyqtSlot(name='show_context_dock')
    def show_context_dock(self):
        self.context_dock.show()

    @pyqtSlot(name='import_elements')
    def import_elements(self):
        '''
        подгружает новые классы из папки
        :return: ничего
        '''
        dir_path = QFileDialog.getExistingDirectory(self, 'Open directory with elements',
                                                    os.path.dirname(__file__), QFileDialog.ShowDirsOnly)
        if dir_path and dir_path != '':
            self.env.import_classes_from_dir(dir_path)
            self.class_model.setData(0, self.env.imported_classes)
            self.update()

    @pyqtSlot(name='save_to_xml')
    def save_to_xml(self):
        path = QFileDialog.getSaveFileName(self, 'Save file',
                                           os.path.dirname(os.path.dirname(__file__)), "XML Files (*.xml)")[0]

        if path and path != '':
            self.env.save_to_xml(path)

    @pyqtSlot(name='open_xml')
    def open_xml(self):
        path = QFileDialog.getOpenFileName(self, 'Open file',
                                           os.path.dirname(os.path.dirname(__file__)), "XML Files (*.xml)")[0]

        if path and path != '':
            try:
                self.env.parse_xml(path)
                self.update_context()
            except Exception as e:
                msg = QMessageBox(self, )
                msg.setWindowTitle("Import Error")
                msg.setText(str(e.args[0]))
                msg.addButton(QMessageBox.Ok)
                msg.setDefaultButton(QMessageBox.Ok)
                msg.show()

            self.update()

    @pyqtSlot(name='start_simulation')
    def start_simulation(self):
        self.update_context(False)

        start_time = float(self.start_time_line_edit.text())
        end_time = float(self.end_time_line_edit.text())
        time_step = float(self.interval_time_line_edit.text())

        try:
            self.statusBar().showMessage("running")
            self.env.run_simulation(start_time, end_time, time_step, self.context)
        except Exception as e:
            msg = QMessageBox(self, )
            msg.setWindowTitle("Run Error")
            msg.setText(str(e.args[0]))
            msg.addButton(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)
            msg.show()

        self.update_context()
        self.statusBar().showMessage("done")