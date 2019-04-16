from PySimCore import ElementPartEnum as EPE, SimBaseClass, OutputSocket, InputSocket, SimConnection,\
    SimCompositeElement, Environment
from ToolsStrategies import MoveTool, ResizeTool, ObserverTool
from typing import Union

class ToolManager:
    def __init__(self, environment: Environment):
        self.env = environment
        self.state = ObserverTool(self.env.cmp)
        self.selected_element = None
        self.element_part = EPE.NONE

    def reset(self):
        self.state = ObserverTool(self.env.cmp)

    def mouse_down(self, x: int, y: int):
        x, y = x - self.env.cmp.x, y - self.env.cmp.y
        self.state.mouse_down(x, y)
        self.change_state(x, y)

    def mouse_unpressed_move(self, x: int, y: int):

        if type(self.selected_element) is not SimCompositeElement:
            x, y = x - self.env.cmp.x, y - self.env.cmp.y

        self.element_part = self.state.mouse_unpressed_move(x, y)

    def mouse_pressed_move(self, x: int, y: int):

        if type(self.selected_element) is not SimCompositeElement:
            x, y = x - self.env.cmp.x, y - self.env.cmp.y

        self.state.mouse_pressed_move(x, y)

    def mouse_double_click(self, x: int, y: int):

        if type(self.selected_element) is not SimCompositeElement:
            x, y = x - self.env.cmp.x, y - self.env.cmp.y

        element, part = self.state.mouse_double_click(x, y)
        self.selected_element = element

    def mouse_up(self, x: int, y: int):

        if type(self.selected_element) is not SimCompositeElement:
            x, y = x - self.env.cmp.x, y - self.env.cmp.y

        self.state.mouse_up(x, y)
        self.state = ObserverTool(self.env.cmp)
        self.element_part = EPE.NONE
        self.selected_element = None

    # ***********************************************************

    def get_element_part(self)->EPE:
        return self.element_part

    def get_element(self)-> Union[SimBaseClass, None]:
        if self.selected_element is not None \
                and issubclass(type(self.selected_element), SimBaseClass) \
                and type(self.selected_element) is not SimCompositeElement:
            return self.selected_element
        return None

    def change_state(self, x: int, y: int):
        element, part = self.env.cmp.find_anything_by_coord(x, y)

        if element is None:  # moving all
            self.state = MoveTool(self.env.cmp, x + self.env.cmp.x, y + self.env.cmp.y)
            self.element_part = EPE.CENTER
            self.selected_element = self.env.cmp
            return
        elif issubclass(type(element), SimBaseClass):
            if part == EPE.CENTER:
                self.state = MoveTool(element, x, y)
            else:
                self.state = ResizeTool(element, part, x, y)
            self.element_part = part

        elif type(element) is SimConnection:
            element.move_to(element.start_box.x, element.start_box.y)
            element.resize(element.end_box.x, element.end_box.y)

            if part == EPE.START:  # moving start
                self.state = MoveTool(element, x, y)
            elif part == EPE.END:  # moving end
                self.state = ResizeTool(element, EPE.NONE, x, y)

            self.element_part = EPE.NONE

        elif type(element) in [InputSocket, OutputSocket]:
            x, y = x - self.env.cmp.x, y - self.env.cmp.y
            connection = SimConnection(self.env.cmp, x, y, x, y)
            self.env.cmp.add_connection(connection)
            if type(element) is InputSocket:
                    connection.set_input_socket(element)
                    self.state = MoveTool(connection, x, y)
            elif type(element) is OutputSocket:
                connection.set_output_socket(element)
                self.state = ResizeTool(connection, EPE.NONE, x, y)

        self.selected_element = element
