from enum import Enum, auto


class Symbol(Enum):
    One = auto()  # spacja pomiedzy ".", "-"
    Three = auto()  # spacja pomiedzy literami
    Seven = auto()  # spacja pomiedzy slowami
    Dot = '.'
    Dash = '-'
