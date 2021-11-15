import json

from pathlib import Path

path = Path(__file__).parent / 'static/morse-code-dict.json'
with path.open() as f:
    MORSE_CODE_DICT = json.load(f)


def encrypt_to_morse(message):
    cipher = ''
    for letter in message:
        if letter != ' ':

            # Looks up the dictionary and adds the
            # correspponding morse code
            # along with a space to separate
            # morse codes for different characters
            cipher += MORSE_CODE_DICT[letter] + ' '
        else:
            # 1 space indicates different characters
            # and 2 indicates different words
            cipher += ' '

    return cipher
