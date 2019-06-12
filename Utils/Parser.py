from abc import ABC, abstractmethod
from PySimCore import Environment


class Parser(ABC):
    @staticmethod
    @abstractmethod
    def save(environment: Environment, path: str):
        pass

    @staticmethod
    @abstractmethod
    def parse(path: str, import_directories: list)-> Environment:
        pass

