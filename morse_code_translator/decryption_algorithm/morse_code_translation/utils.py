import json
from pathlib import Path


def load_morse_code_dict() -> dict:

    path = Path(__file__).parent / 'static/morse-code-dict.json'
    with path.open() as f:
        return json.load(f)