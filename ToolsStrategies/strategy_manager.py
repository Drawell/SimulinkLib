from Environment.environment import Environment
from SimElement.element_part_enum import ElementPartEnum as EPE
from SimElement.sim_base_class import SimBaseClass
from SimElement.sim_socket import OutputSocket, InputSocket
from SimElement.sim_connection import SimConnection

from ToolsStrategies.move_tool import MoveTool
from ToolsStrategies.resize_tool import ResizeTool
from ToolsStrategies.observer_tool import ObserverTool
from ToolsStrategies.line_drawer_tool import LineDrawerTool

class StrategyManager:
    def __init__(self, env: Environment):
        self.env = env

    def get_default_strategy(self):
        return ObserverTool(self.env)

    def get_strategy(self, x: int, y: int) -> tuple:
        element, part = self.env.get_element_by_coord(x, y)
        print(x, y, element)
        # moving all
        if element is None or part == EPE.NONE:
            return MoveTool(self.env, x, y), EPE.CENTER
        elif issubclass(type(element), SimBaseClass):
            if part == EPE.CENTER:
                return MoveTool(element, x, y), EPE.CENTER
            return ResizeTool(element, part, x, y), part

        elif type(element) is InputSocket:
            connection = SimConnection(self.env, x, y, x, y)
            self.env.add_connection(connection)
            self.env.try_to_connect(connection)
            box = connection.get_start_box()
            return LineDrawerTool(x, y, connection, box, self.env), EPE.CENTER

        elif type(element) is OutputSocket:
            connection = SimConnection(self.env, x, y, x, y)
            self.env.add_connection(connection)
            self.env.try_to_connect(connection)
            box = connection.get_end_box()
            return LineDrawerTool(x, y, connection, box, self.env), EPE.CENTER

        elif type(element) is SimConnection:  # bad
            return LineDrawerTool(x, y, element, part, self.env), EPE.CENTER

        return ObserverTool(self.env), EPE.NONE
