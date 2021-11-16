import logging
from random import seed, randint
from typing import Optional

from morse_code_translation import decrypt_from_morse
from morse_code_translation import encrypt_to_morse
from morse_code_symbol import MorseCodeSymbol

# constants
TIME_UNIT = 1
INTERVAL = 0.1
CHARACTERS_PER_TIME_UNIT = int(TIME_UNIT / INTERVAL)
MARGIN_OF_ERROR = 3

# logger
logging.basicConfig(filename='algorithm.log',
                    filemode='w',
                    format='[%(filename)s:%(lineno)d %(levelname)s] %(message)s\t',
                    level=logging.DEBUG)


def translate_numbers_to_enum(arduino_substring: str, click_index: int) -> Optional[MorseCodeSymbol]:
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

    :param arduino_substring: ciag znakow samych zer albo jedynek pobrany do interpretacji
    :param click_index: indeks kolejnych klikniec
    :return: enum typu MorseCodeSymbol
    """
    if click_index % 2 != 0:
        if abs(len(arduino_substring) - CHARACTERS_PER_TIME_UNIT) <= MARGIN_OF_ERROR:  # spacja pomiedzy "." a "-"
            return MorseCodeSymbol.One
        elif abs(len(arduino_substring) - 3 * CHARACTERS_PER_TIME_UNIT) <= MARGIN_OF_ERROR:  # spacja pomiedzy literami
            return MorseCodeSymbol.Three
        elif abs(len(arduino_substring) - 7 * CHARACTERS_PER_TIME_UNIT) <= MARGIN_OF_ERROR:  # spacja pomiedzy slowami
            return MorseCodeSymbol.Seven
        else:
            print(
                '\t(Disclaimer): poczatkowy ciag znakow prawdopodobnie bedzie wykraczal poza ustalony margines bledu.\n')
            return MorseCodeSymbol.Default

    else:
        if abs(len(arduino_substring) - CHARACTERS_PER_TIME_UNIT) <= MARGIN_OF_ERROR:  # "."
            return MorseCodeSymbol.Dot
        elif abs(len(arduino_substring) - 3 * CHARACTERS_PER_TIME_UNIT) <= MARGIN_OF_ERROR:  # "-"
            return MorseCodeSymbol.Dash
        elif abs(len(arduino_substring) - 7 * CHARACTERS_PER_TIME_UNIT) <= MARGIN_OF_ERROR:  # spacja pomiedzy slowami
            return MorseCodeSymbol.Seven
        else:
            raise Exception(f'Przekroczono mozliwy margines bledu, liczba znakow: {len(arduino_substring)}')


def convert_from_morse_to_arduino(morse_code: str) -> str:
    decrypt_from_morse(morse_code)
    result = 14 * '1'  # imitacja tego co arduino wyrzuci zanim zaczniemy tlumaczyc faktyczny input
    toggle = 0
    for idx, symbol in enumerate(morse_code):
        seed(1)
        if symbol == '.':
            result += randint(CHARACTERS_PER_TIME_UNIT - MARGIN_OF_ERROR,
                              CHARACTERS_PER_TIME_UNIT + MARGIN_OF_ERROR) * str(toggle)
        elif symbol == '-':
            result += randint(CHARACTERS_PER_TIME_UNIT * 3 - MARGIN_OF_ERROR,
                              CHARACTERS_PER_TIME_UNIT * 3 + MARGIN_OF_ERROR) * str(toggle)
        elif symbol == ' ':
            result += randint(CHARACTERS_PER_TIME_UNIT * 7 - MARGIN_OF_ERROR,
                              CHARACTERS_PER_TIME_UNIT * 7 + MARGIN_OF_ERROR) * str(toggle)
        else:
            raise Exception('Niespodziewana wartosc')

        # dodanie spacji po symbolu "." lub "-"
        if idx + 1 < len(morse_code) - 1:
            if morse_code[idx] != ' ' and morse_code[idx + 1] != ' ':
                toggle = (int(toggle) + 1) % 2
                result += randint(CHARACTERS_PER_TIME_UNIT - MARGIN_OF_ERROR,
                                  CHARACTERS_PER_TIME_UNIT + MARGIN_OF_ERROR) * str(toggle)

        toggle = (int(toggle) + 1) % 2

    return result


def convert_from_arduino_to_morse(arduino_data: str) -> str:
    result_in_morse = ''
    result_in_english = ''
    click_index = 0  # ktore to klikniecie z kolei
    temp_val = arduino_data[0]  # poczatkowa wartosc (0 lub 1) potrzebna do sprawdzania kiedy ciag ulegl zmianie
    end_of_substring_index = 0
    nr_of_spaces = 0  # potrzebne do przypadku dla spacji pomiedzy slowami, czyli wystapeinia 2x Symbols.Seven po sobie
    for idx, val in enumerate(arduino_data):
        if temp_val != val:
            click_index += 1
            if nr_of_spaces == 2:
                result_in_english += ' '  # skoro 2x MorseCodeSymbol.Seven -> dodajemy spacje do rezultatu
                # resetujemy indeks klikniec prez zalozenie parzystosci (patrz translate_numbers_to_enum)
                click_index = 0
            result = translate_numbers_to_enum(arduino_data[end_of_substring_index:idx], click_index)
            logging.info(
                f'Click_index = {click_index}, substring = {arduino_data[end_of_substring_index:idx]}, '
                f'length: {len(arduino_data[end_of_substring_index:idx])}, '
                f'result: Enum -> {result}, Value -> {result.value}')
            if result == MorseCodeSymbol.Dot or result == MorseCodeSymbol.Dash:
                nr_of_spaces = 0
                result_in_morse += result.value
            elif result == MorseCodeSymbol.Three:  # MorseCodeSymbol.Three - spacja pomiedzy literami
                nr_of_spaces = 0
                result_in_english += decrypt_from_morse(
                    result_in_morse.upper())  # skoro ltera gotowa, mozna rozszyfrowac
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

    text_in_arduino = convert_from_morse_to_arduino(encrypted)
    print(f'3. Text converted from morse code to possible arduino-alike:\n\t{text_in_arduino}')

    decrypted = decrypt_from_morse(convert_from_arduino_to_morse(text_in_arduino))
    print(f'4. [FINAL] Decrypted text from arduino-alike to human-alike:\n\t{decrypted}\n')


if __name__ == '__main__':
    main()
