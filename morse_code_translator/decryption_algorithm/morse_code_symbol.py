from enum import Enum, unique


# value dla One, Three, Seven i Default nie jest auto() dla przejrzystych logow
@unique
class MorseCodeSymbol(Enum):
    One = 'MorseCodeSymbol.One'  # spacja pomiedzy ".", "-"
    Three = 'MorseCodeSymbol.Three'  # spacja pomiedzy literami
    Seven = 'MorseCodeSymbol.Seven'  # spacja pomiedzy slowami
    Dot = '.'
    Dash = '-'
    Default = 'MorseCodeSymbol.Default'
