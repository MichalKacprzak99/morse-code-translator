import logging
from random import randint
from typing import Optional

from morse_code_symbol import MorseCodeSymbol
from morse_code_translation import decrypt_from_morse
from morse_code_translation import encrypt_to_morse

# constants
MARGIN_OF_ERROR = 3
GAP_BETWEEN_SYMBOLS = 1
GAP_BETWEEN_LETTERS = 3
GAP_BETWEEN_WORDS = 7

# logger
logging.basicConfig(filename='algorithm.log',
                    filemode='w',
                    format='[%(filename)s:%(lineno)d %(levelname)s] %(message)s\t',
                    level=logging.DEBUG)


def translate_numbers_to_enum(arduino_substring: str, click_index: int,
                              characters_per_time_unit: int) -> Optional[MorseCodeSymbol]:
    """
    W zaleznosci od tego ktore to z kolei klikniecie, inaczej jest interpretowany ciag znakow.
    Zakladamy ze poczatkowy ciag znakow jakie wyrzuca arduino nie jest brany pod uwage do translacji,
    wiec zostanie pominiety. Kliknieciem rozpoczynamy "zabawe" i po nim mierzymy ciag znakow
    (poczatkowe klikniecie nie inkrementuje click_indexu)

    Kolejne klikniecie skutkuje inkrementacja click_indexu i oznacza, ze przerwalismy mierzenie pierwszego symbolu.
    Po nim nastepuja przerwa danej dlugosc znakow interpretowane jako spacja i kolejne klikniecie.

    Zatem po nieparzystym click_indexie bedzie zawsze spacja -> MorseCodeSymbol.One / MorseCodeSymbol.Three albo MorseCodeSymbol.Seven
    !!! Z wyjatkiem przypadku gdzie mamy spacje po spacji przy oddzieleniu dwoch slow od siebie, ten przypadek jest
    obsluzony w linii 94, (dlatego liczenie spacji nastepujacych po sobie bylo konieczne)

    :param characters_per_time_unit: how ma
    :param arduino_substring: ciag znakow samych zer albo jedynek pobrany do interpretacji
    :param click_index: indeks kolejnych klikniec
    :return: enum typu MorseCodeSymbol
    """
    gap_to_symbols = {
        GAP_BETWEEN_SYMBOLS: MorseCodeSymbol.One if click_index % 2 != 0 else MorseCodeSymbol.Dot,  # space beetween "." and "-" or '.'
        GAP_BETWEEN_LETTERS: MorseCodeSymbol.Three if click_index % 2 != 0 else MorseCodeSymbol.Dash, # space beetween letters or "-"
        GAP_BETWEEN_WORDS: MorseCodeSymbol.Seven,  # space between words
    }

    for gap, symbol in gap_to_symbols.items():
        if abs(len(arduino_substring) - gap * characters_per_time_unit) <= MARGIN_OF_ERROR:  # spacja pomiedzy "." a "-"
            return symbol
    else:
        if click_index % 2 == 0:
            raise Exception(f'Przekroczono mozliwy margines bledu, liczba znakow: {len(arduino_substring)}')
        else:
            print('\t(Disclaimer): poczatkowy ciag znakow prawdopodobnie bedzie wykraczal poza ustalony margines bledu.\n')
            return MorseCodeSymbol.Default


def convert_from_morse_to_arduino(morse_code: str, time_unit: float, interval: float) -> str:
    decrypt_from_morse(morse_code)
    result = 14 * '1'  # imitacja tego co arduino wyrzuci zanim zaczniemy tlumaczyc faktyczny input
    toggle = 0
    characters_per_time_unit = int(time_unit / interval)
    symbol_to_gap = {
        '.': GAP_BETWEEN_SYMBOLS,
        '-': GAP_BETWEEN_LETTERS,
        ' ': GAP_BETWEEN_WORDS,
    }

    for idx, symbol in enumerate(morse_code):
        error = randint(-MARGIN_OF_ERROR, +MARGIN_OF_ERROR)
        result += (characters_per_time_unit * symbol_to_gap.get(symbol) + error) * str(toggle)

        # dodanie spacji po symbolu "." lub "-"
        if idx + 1 < len(morse_code) - 1:
            if morse_code[idx] != ' ' and morse_code[idx + 1] != ' ':
                toggle = (toggle + 1) % 2
                result += randint(characters_per_time_unit - MARGIN_OF_ERROR,
                                  characters_per_time_unit + MARGIN_OF_ERROR) * str(toggle)

        toggle = (toggle + 1) % 2

    return result


def convert_from_arduino_to_morse(arduino_data: str, time_unit: float, interval: float) -> str:
    result_in_morse = ''
    click_index = 0  # ktore to klikniecie z kolei
    temp_val = arduino_data[0]  # poczatkowa wartosc (0 lub 1) potrzebna do sprawdzania kiedy ciag ulegl zmianie
    end_of_substring_index = 0
    nr_of_spaces = 0  # potrzebne do przypadku dla spacji pomiedzy slowami, czyli wystapeinia 2x Symbols.Seven po sobie
    characters_per_unit = int(time_unit / interval)

    for idx, val in enumerate(arduino_data):
        if temp_val != val:
            click_index += 1
            if nr_of_spaces == 2:
                click_index = 0
            result = translate_numbers_to_enum(arduino_substring=arduino_data[end_of_substring_index:idx],
                                               click_index=click_index,
                                               characters_per_time_unit=characters_per_unit)
            logging.info(
                f'Click_index = {click_index}, substring = {arduino_data[end_of_substring_index:idx]}, '
                f'length: {len(arduino_data[end_of_substring_index:idx])}, '
                f'result: Enum -> {result}, Value -> {result.value}')
            if result in [MorseCodeSymbol.Dot, MorseCodeSymbol.Dash]:
                nr_of_spaces = 0
                result_in_morse += result.value
            elif result == MorseCodeSymbol.Three:  # MorseCodeSymbol.Three - spacja pomiedzy literami
                nr_of_spaces = 0
                result_in_morse = ''  # resetujemy zmienna trzymajaca symbole
            elif result == MorseCodeSymbol.Seven:  # MorseCodeSymbol.Seven - spacja pomiedzy slowami
                nr_of_spaces += 1
                result_in_morse += ' '
            else:
                nr_of_spaces = 0
            temp_val = val
            end_of_substring_index = idx

    return result_in_morse


def main():
    text = "Nigdy nie jedz U Szwagra"
    print(f'1. Original human-like text:\n\t{text}\n')

    encrypted = encrypt_to_morse(text.upper())
    print(f'2. Encrypted text (in morse code):\n\t{encrypted}\n')

    text_in_arduino = convert_from_morse_to_arduino(morse_code=encrypted, time_unit=1, interval=0.1)
    print(f'3. Text converted from morse code to possible arduino-alike:\n\t{text_in_arduino}')

    decrypted = decrypt_from_morse(convert_from_arduino_to_morse(arduino_data=text_in_arduino,
                                                                 time_unit=1, interval=0.1))
    print(f'4. [FINAL] Decrypted text from arduino-alike to human-alike:\n\t{decrypted}\n')


if __name__ in '__main__':
    main()
