import logging
from random import randint
from typing import Optional, Tuple

from morse_code_translator.decryption_algorithm.morse_code_symbol import MorseCodeSymbol
from morse_code_translator.decryption_algorithm.morse_code_translation import decrypt_from_morse
from morse_code_translator.decryption_algorithm.morse_code_translation import encrypt_to_morse
from morse_code_translator.decryption_algorithm.morse_code_translation.utils import load_morse_code_dict

MORSE_CODE_DICT = load_morse_code_dict()

# constants
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
    Depending on click index, characters' stream substring is interpreted differently.
    Moreover, we assume that initial stream is not taken into consideration because until we start the process of
    translation, it is not important therefore it is ignored.
    With the first click, we start the process of receiving each substring (initial click does not increment
    click_index).

    The next click increments click_index and means that the process of receiving first symbol's data is done.
    After that, the break of particular length occurs (length of the break is relevant) which stands for gap between
    symbols, letters or words depending on its length and another click should take place.

    Therefore, after every odd click_index there will be a space represented by one of these enum values:
    MorseCodeSymbol.One - space between symbols
    MorseCodeSymbol.Three - space between letters
    MorseCodeSymbol.Seven - space between words
    !!!
    With the exception where space after space occurs, which should take place when the user wants to separate words
    from each other. Such case is handled separately.

    :param characters_per_time_unit: how ma
    :param arduino_substring: stream of 0's or 1's received for interpretation
    :param click_index: ordinal number of clicks
    :return: enum representing each symbol
    """
    error_margin = int(characters_per_time_unit * 30 / 100)
    gap_to_symbols = {
        # space between "." and "-" or '.'
        GAP_BETWEEN_SYMBOLS: MorseCodeSymbol.One if click_index % 2 != 0 else MorseCodeSymbol.Dot,
        # space between letters or "-"
        GAP_BETWEEN_LETTERS: MorseCodeSymbol.Three if click_index % 2 != 0 else MorseCodeSymbol.Dash,
        # space between words
        GAP_BETWEEN_WORDS: MorseCodeSymbol.Seven,
    }

    for gap, symbol in gap_to_symbols.items():
        if abs(len(arduino_substring) - gap * characters_per_time_unit) <= error_margin:  # space between '.' or '-
            return symbol
    else:
        if click_index % 2 == 0:
            print(f'\tMaximum margin of error exceeded, string length: {len(arduino_substring)}')
            return MorseCodeSymbol.Error
        else:
            print(
                '\t(Disclaimer): initial characters stream will probably exceed maximum margin of error.')
            return MorseCodeSymbol.Default


def convert_from_morse_to_arduino(morse_code: str, time_unit: float, interval: float) -> str:
    decrypt_from_morse(morse_code)
    result = 14 * '1'  # imitate what arduino might send before we start translating its data
    toggle = 0
    characters_per_time_unit = int(time_unit / interval)
    error_margin = int(characters_per_time_unit * 30 / 100)
    symbol_to_gap = {
        '.': GAP_BETWEEN_SYMBOLS,
        '-': GAP_BETWEEN_LETTERS,
    }
    omit_flag = False

    for idx, symbol in enumerate(morse_code):
        if omit_flag:
            omit_flag = False
            continue

        if symbol != ' ':
            error = randint(-error_margin, +error_margin)
            result += (characters_per_time_unit * symbol_to_gap.get(symbol) + error) * str(toggle)
            # appending space after "." or "-"
            if idx + 1 < len(morse_code) - 1:
                if morse_code[idx + 1] != ' ':
                    toggle = (toggle + 1) % 2
                    result += randint(characters_per_time_unit - error_margin,
                                      characters_per_time_unit + error_margin) * str(toggle)
        # handle space symbol
        else:
            if idx + 1 < len(morse_code) - 1:
                # if next symbol is space as well, append gap=7 and omit adding next symbol
                if morse_code[idx + 1] == ' ':
                    omit_flag = True
                    gap = GAP_BETWEEN_WORDS
                else:
                    gap = GAP_BETWEEN_LETTERS
            else:
                gap = GAP_BETWEEN_LETTERS

            result += randint(characters_per_time_unit * gap - error_margin,
                              characters_per_time_unit * gap + error_margin) * str(toggle)

        toggle = (toggle + 1) % 2
    return result


def convert_from_arduino_to_morse(arduino_data: str, time_unit: float, interval: float) -> Tuple[str, dict]:
    result_in_morse = ''
    click_index = 0  # index of each click
    temp_val = arduino_data[0]  # initial value (0 or 1) needed to check the stream changed
    end_of_substring_index = 0
    characters_per_unit = int(time_unit / interval)
    error_margin = int(characters_per_unit * 30 / 100)
    stats = {
        'characters_per_unit': characters_per_unit,
        'error_margin': error_margin,
        'dot': {
            "data": [],
            "symbol_characters": 1
        },
        'dash': {
            "data": [],
            "symbol_characters": 3
        },
        'space_symbols': {
            "data": [],
            "symbol_characters": GAP_BETWEEN_SYMBOLS
        },
        'space_letters': {
            "data": [],
            "symbol_characters": GAP_BETWEEN_LETTERS
        },
        'space_words': {
            "data": [],
            "symbol_characters": GAP_BETWEEN_WORDS
        },
    }

    enum_to_stats_key = {
        MorseCodeSymbol.Dot: 'dot',
        MorseCodeSymbol.Dash: 'dash',
        MorseCodeSymbol.One: 'space_symbols',
        MorseCodeSymbol.Three: 'space_letters',
        MorseCodeSymbol.Seven: 'space_words',
        MorseCodeSymbol.Error: 'error'
    }

    for idx, val in enumerate(arduino_data):
        if temp_val != val:
            click_index += 1
            result = translate_numbers_to_enum(arduino_substring=arduino_data[end_of_substring_index:idx],
                                               click_index=click_index,
                                               characters_per_time_unit=characters_per_unit)
            logging.info(
                f'Click_index = {click_index}, substring = {arduino_data[end_of_substring_index:idx]}, '
                f'length: {len(arduino_data[end_of_substring_index:idx])}, '
                f'result: Enum -> {result}, Value -> {result.value}')

            # append data to stats object
            try:
                stats[enum_to_stats_key.get(result)].get("data").append(
                    len(arduino_data[end_of_substring_index:idx])
                )
            except KeyError:
                print(f'\tKey: {result} in enum_to_stats_key not found.\n')

            if result in [MorseCodeSymbol.Dot, MorseCodeSymbol.Dash]:
                result_in_morse += result.value
            elif result == MorseCodeSymbol.Three:  # space between letters
                result_in_morse += ' '
            elif result == MorseCodeSymbol.Seven:  # space between words
                result_in_morse += '  '
            elif result == MorseCodeSymbol.Error:
                result_in_morse = result_in_morse.strip() + ' ' + MORSE_CODE_DICT.get(MorseCodeSymbol.Error.value)
            temp_val = val
            end_of_substring_index = idx

    return result_in_morse.strip(), stats


def main():
    text = "This is AGH"
    print(f'1. Original human-like text:\n\t{text}\n')

    encrypted = encrypt_to_morse(text.upper())
    print(f'2. Encrypted text (in morse code):\n\t{encrypted}\n')

    text_in_arduino = convert_from_morse_to_arduino(morse_code=encrypted, time_unit=1, interval=0.1)
    print(f'3. Text converted from morse code to possible arduino-alike:\n\t{text_in_arduino}')

    morse_code_from_arduino, result = convert_from_arduino_to_morse(arduino_data=text_in_arduino,
                                                                    time_unit=1, interval=0.1)
    print(f'4. [Morse] Decrypted text from arduino-alike to morse-alike:\n\t{morse_code_from_arduino}\n')

    decrypted = decrypt_from_morse(morse_code_from_arduino)
    print(f'4. [FINAL] Decrypted text from morse to human-alike:\n\t{decrypted}\n')


if __name__ in '__main__':
    main()
