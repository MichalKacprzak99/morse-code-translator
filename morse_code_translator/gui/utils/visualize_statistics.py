from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


def visualize_translation_statistics(translation_statistics: dict, save_statistics_to: Path):
    error_margin = translation_statistics.pop("error_margin")
    characters_per_unit = translation_statistics.pop("characters_per_unit")

    analyzed_statistics = []

    for symbol, symbol_data in translation_statistics.items():
        symbol_characters = symbol_data.get("symbol_characters")
        data = symbol_data.get("data")
        mean = np.round(np.mean(data), 2) if data else f"No data"
        std = np.round(np.std(data, axis=0), 2) if data else f"No data"
        exact_value = characters_per_unit * symbol_characters
        error = np.abs(exact_value - np.array(data))

        relative_error = f"{np.round(np.mean(error / exact_value) * 100, 2)}%" if data else f"No data"

        analyzed_statistics.append([
            symbol.replace('_', ' ').capitalize(),
            exact_value,
            mean,
            std,
            relative_error
        ])

    fig, (ax1, ax2) = plt.subplots(2, 1)
    title = f"Morse code translation analysis: error margin = {error_margin}, characters per unit = {characters_per_unit}"
    fig.suptitle(title, fontsize=20)
    fig.set_size_inches(12, 12)

    column_labels = ("Morse Symbol", "Exact Value", "Mean", "Standard Deviation", "Relative error")

    ax1.axis('off')
    table = ax1.table(cellText=analyzed_statistics,
                      colLabels=column_labels,
                      loc='upper center',
                      cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(15)

    table.scale(1.2, 4)

    bar_column_names = [symbol.replace('_', ' ').replace('between', '').capitalize()
                        for symbol in translation_statistics.keys()]
    bar_values = [len(symbol_data.get("data")) for symbol_data in translation_statistics.values()]
    idx = np.asarray([i for i in range(len(bar_values))])
    ax2.bar(idx, bar_values, 0.3)

    ax2.set_xticks(idx)
    ax2.set_xticklabels(bar_column_names, fontsize=17)
    ax2.set_title('Number of sumbols', fontsize=20)
    ax2.set_xlabel('Symbols', fontsize=25)
    ax2.set_ylabel('Number of counts', fontsize=20)

    plt.savefig(save_statistics_to / 'translation_statistics.jpg')


if __name__ == '__main__':
    visualize_translation_statistics(translation_statistics={
        'characters_per_unit': 10,
        "error_margin": 3,
        "dot": {
            "data": [
                12,
                11,
                7,
                9,
                10,
                12,
                11,
                8,
                7,
                10,
                8,
                7,
                7,
                10,
                7,
                9,
                8,
                8,
                12,
                7,
                10,
                12,
                12
            ],
            "symbol_characters": 1
        },
        "dash": {
            "data": [
                30,
                27,
                32,
                32,
                31,
                32,
                28
            ],
            "symbol_characters": 3
        },
        "space_symbols": {
            "data": [
                9,
                10,
                12,
                9,
                13,
                9,
                12,
                10,
                8,
                13,
                7,
                10,
                11,
                8,
                9,
                13,
                10,
                12
            ],
            "symbol_characters": 1
        },
        "space_letters": {
            "data": [
                28,
                32,
                28,
                31,
                32,
                28,
                29,
                27,
                32
            ],
            "symbol_characters": 3
        },
        "space_words": {
            "data": [
                72,
                73
            ],
            "symbol_characters": 7
        }
    }, save_statistics_to=Path())
