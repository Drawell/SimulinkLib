from abc import ABC, abstractmethod
import cairo
from io import BytesIO

class SimBaseClass(ABC):
    def __init__(self, x: int, y: int, kwargs):
        super().__init__()
        self.x = x
        self.y = y
        self.name = kwargs['name'] if 'name' in kwargs else 'Scope'
        self.width = kwargs['width'] if 'width' in kwargs else 50
        self.height = kwargs['height'] if 'height' in kwargs else 50

    def move_to(self, x: int, y: int):
        self.x = x
        self.y = y

    def resize(self, w: int, h: int):
        self.width = max(w, 32)
        self.height = max(h, 32)

    @abstractmethod
    def make_step(self, time: float):
        pass

    @staticmethod
    def get_base_img_as_surface(w: int, h: int):
        pass

    @staticmethod
    def get_base_img_as_byte_data(w: int, h: int):
        pass

    @staticmethod
    def get_img_path()->str:
        pass

    @staticmethod
    def get_name()->str:
        pass

    @staticmethod
    def get_data_from_surface(surface)-> bytes:
        with BytesIO() as b:
            surface.write_to_png(b)
            b.seek(0)
            data = b.read()

        return data

    @abstractmethod
    def get_img_as_surface(self, w: int, h: int):
        pass

    def get_img_as_byte_data(self, w: int, h: int):
        surface = self.get_img_as_surface(w, h)
        return SimBaseClass.get_data_from_surface(surface)