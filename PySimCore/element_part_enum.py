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


class SocketPositionEnum(enum.Enum):
    TOP = 'TOP'
    BOTTOM = 'BOTTOM'
    RIGHT = 'RIGHT'
    LEFT = 'LEFT'

    def __invert__(other):
        if other == SocketPositionEnum.TOP:    return SocketPositionEnum.BOTTOM
        if other == SocketPositionEnum.BOTTOM: return SocketPositionEnum.TOP
        if other == SocketPositionEnum.RIGHT:  return SocketPositionEnum.LEFT
        if other == SocketPositionEnum.LEFT:   return SocketPositionEnum.RIGHT
