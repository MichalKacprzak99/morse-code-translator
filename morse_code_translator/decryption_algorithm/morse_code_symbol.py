from enum import Enum, unique


@unique
class MorseCodeSymbol(Enum):
    One = 'MorseCodeSymbol.One'  # space between "." or "-"
    Three = 'MorseCodeSymbol.Three'  # space between letters
    Seven = 'MorseCodeSymbol.Seven'  # space between words
    Dot = '.'
    Dash = '-'
    Default = 'MorseCodeSymbol.Default'
    Error = '?'
