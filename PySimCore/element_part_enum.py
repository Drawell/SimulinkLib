import enum


class ElementPartEnum(enum.Enum):
    NONE = 'NONE'
    CENTER = 'CENTER'
    TOP = 'TOP'
    BOTTOM = 'BOTTOM'
    RIGHT = 'RIGHT'
    LEFT = 'LEFT'
    TOP_RIGHT = 'TOP_RIGHT'
    TOP_LEFT = 'TOP_LEFT'
    BOTTOM_RIGHT = 'BOTTOM_RIGHT'
    BOTTOM_LEFT = 'BOTTOM_LEFT'
    START = 'START'
    END = 'END'


class RotationPositionEnum(enum.Enum):
    TOP = 'TOP'
    BOTTOM = 'BOTTOM'
    RIGHT = 'RIGHT'
    LEFT = 'LEFT'
