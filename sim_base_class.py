from abc import ABC, abstractmethod


class SimBaseClass:
    def __init__(self, x: int, y: int):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50

    def move_to(self, x: int, y: int):
        self.x = x
        self.y = y

    def resize(self, w: int, h: int):
        self.width = w
        self.height = h

    @abstractmethod
    def make_step(self):
        pass

    @staticmethod
    def get_img_path()->str:
        pass

    @staticmethod
    def get_name()->str:
        pass
