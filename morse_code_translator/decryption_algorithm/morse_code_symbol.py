from enum import Enum


# value dla One, Three, Seven i Default nie jest auto() dla przejrzystych logow

class MorseCodeSymbol(Enum):
    One = 'MorseCodeSymbol.One'  # spacja pomiedzy ".", "-"
    Three = 'MorseCodeSymbol.Three'  # spacja pomiedzy literami
    Seven = 'MorseCodeSymbol.Seven'  # spacja pomiedzy slowami
    Dot = '.'
    Dash = '-'
    Default = 'MorseCodeSymbol.Default'
