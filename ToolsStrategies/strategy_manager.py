from Environment.environment import Environment
from SimElement.element_part_enum import ElementPartEnum as EPE
from ToolsStrategies.base_strategy import BaseStrategy
from ToolsStrategies.move_tool import MoveTool
from ToolsStrategies.resize_tool import ResizeTool
from ToolsStrategies.observer_tool import ObserverTool

class StrategyManager:
    def __init__(self, env: Environment):
        self.env = env

    def get_default_strategy(self):
        return ObserverTool(self.env)

    def get_strategy(self, x: int, y: int) -> tuple:
        element, part = self.env.get_element_by_coord(x, y)
        if element is None or part == EPE.NONE:
            return MoveTool(self.env, x, y), EPE.CENTER

        if part == EPE.CENTER:
            return MoveTool(element, x, y), EPE.CENTER

        return ResizeTool(element, part, x, y), part
