from Environment import Environment
from PySimCore import ElementPartEnum as EPE, SimBaseClass, OutputSocket, InputSocket, SimConnection
from ToolsStrategies import MoveTool, ResizeTool, ObserverTool, LineDrawerTool


class StrategyManager:
    def __init__(self):
        #self.env = env
        pass

    @staticmethod
    def get_default_strategy(env):
        return ObserverTool(env)

    @staticmethod
    def get_strategy(env: Environment, x: int, y: int) -> tuple:
        element, part = env.get_element_by_coord(x, y)
        print(x, y, element)
        # moving all
        if element is None or part == EPE.NONE:
            return MoveTool(env, x, y), EPE.CENTER
        elif issubclass(type(element), SimBaseClass):
            if part == EPE.CENTER:
                return MoveTool(element, x, y), EPE.CENTER
            return ResizeTool(element, part, x, y), part

        elif type(element) is InputSocket:
            connection = SimConnection(env, x - env.x, y - env.y, x - env.x, y - env.y)
            env.add_connection(connection)
            env.try_to_connect(connection)
            box = connection.get_start_box()
            return LineDrawerTool(x, y, connection, box, env), EPE.CENTER

        elif type(element) is OutputSocket:
            connection = SimConnection(env, x - env.x, y - env.y, x - env.x, y - env.y)
            env.add_connection(connection)
            env.try_to_connect(connection)
            box = connection.get_end_box()
            return LineDrawerTool(x, y, connection, box, env), EPE.CENTER

        elif type(element) is SimConnection:  # bad
            return LineDrawerTool(x, y, element, part, env), EPE.CENTER

        return ObserverTool(env), EPE.NONE
