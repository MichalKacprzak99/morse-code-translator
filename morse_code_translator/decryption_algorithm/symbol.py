from enum import Enum


# value dla One, Three, Seven i Default nie jest auto() dla przejrzystych logow

class Symbol(Enum):
    One = 'Symbol.One'  # spacja pomiedzy ".", "-"
    Three = 'Symbol.Three'  # spacja pomiedzy literami
    Seven = 'Symbol.Seven'  # spacja pomiedzy slowami
    Dot = '.'
    Dash = '-'
    Default = 'Symbol.Default'
