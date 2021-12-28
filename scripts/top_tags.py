import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import rcParams

PARAMS = {
    'all': {
        'categories': ['genre', 'instrument', 'mood_theme'],
        'n': 20,
        'ylim': 18000,
        'label_idx': [0, 20, 40, 59],
        'label_distance': 1000,
        'y_ticks': np.arange(0, 20_000, 4000),
        'y_suffix': 'k',
    },
    'mood_theme': {
        'categories': ['mood_theme'],
        'n': 56,
        'ylim': 2000,
        'label_idx': [0, 55],
        'label_distance': 100,
        'y_ticks': np.arange(0, 2000, 500),
        'y_suffix': '',
    }
}

SIZES = {
    'wide': {
        'shape': (12, 2),
        'label_distance_multiplier': 1.0,
    },
    'thesis': {
        'shape': (12, 8),
        'label_distance_multiplier': 0.3,
    }
}


def main(plot: str, directory: Path, output_file: Path, shape: str) -> None:
    params = PARAMS[plot]
    sizes = SIZES[shape]

    tag_list = []
    track_list = []

    for category in params['categories']:
        tsv_file = directory / f'{category}.tsv'
        df = pd.read_csv(tsv_file, delimiter='\t')
        df = df.sort_values(by=['tracks'], ascending=False)
        df = df[:params['n']]
        tag_list += list(df['tag'])
        track_list += list(df['tracks'])

    plt.figure(figsize=sizes['shape'])
    plt.style.use('seaborn-whitegrid')

    rcParams['font.family'] = 'serif'
    rcParams['font.serif'] = 'Times New Roman'

    plt.grid(False)
    plt.ylabel('# of tracks')
    plt.xlim([-1, params['n'] * len(params['categories'])])
    plt.ylim([0, params['ylim']])
    for i in range(len(params['categories'])):
        indices = np.arange(params['n'] * i, params['n'] * (i + 1))
        plt.bar(indices, np.array(track_list)[indices], align='center')

    offset = params['label_distance'] * sizes['label_distance_multiplier']
    for i in params['label_idx']:
        plt.text(i, track_list[i] + offset, track_list[i], fontsize=8, horizontalalignment='center')

    plt.xticks(np.arange(len(tag_list)), tag_list, rotation='vertical')
    if params['y_suffix'] == 'k':
        y_labels = ['{}k'.format(y_tick // 1000) for y_tick in params['y_ticks']]
    else:
        y_labels = params['y_ticks']
    plt.yticks(params['y_ticks'], y_labels)
    plt.subplots_adjust(bottom=0.4)

    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    output_file.parent.mkdir(exist_ok=True)
    plt.savefig(output_file, bbox_inches='tight', dpi=150)
    plt.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Plots the top tags according to number of tracks per tag')
    parser.add_argument('plot', choices=PARAMS.keys(), help='which plot to produce')
    parser.add_argument('directory', type=Path, help='stats directory from mtg-jamendo with TSV files')
    parser.add_argument('output_file', type=Path, help='figure output file')
    parser.add_argument('--shape', choices=SIZES.keys(), default='wide', help='figure shape')
    args = parser.parse_args()

    main(args.plot, args.directory, args.output_file, args.shape)
