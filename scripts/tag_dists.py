import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import rcParams


def main(input_dir: Path, tags_file: Path, output_file: Path, category: str) -> None:
    sns.set_style('white')
    rcParams['font.family'] = 'serif'
    rcParams['font.serif'] = 'Times New Roman'

    tags = np.loadtxt(str(tags_file), dtype=str)
    tags = [tag.split('---')[1] for tag in tags]

    fig, axes = plt.subplots(3, 3, figsize=(23, 10), sharex='all')

    for ax_row, split_set in zip(axes, ['train', 'validation', 'test']):
        input_file = input_dir / split_set / f'{category}.tsv'
        df = pd.read_csv(input_file, sep='\t')
        for ax, entity in zip(ax_row, ['tracks', 'artists', 'albums']):
            g = sns.barplot(data=df, x='tag', y=entity, ax=ax, order=tags, palette='deep')
            ax.tick_params(axis='x', rotation=90, labelsize='small')
            g.set(xlabel=None, ylabel=None)

    axes[0][0].set_title('# of tracks')
    axes[0][1].set_title('# of artists')
    axes[0][2].set_title('# of albums')

    axes[0][0].set_ylabel('train')
    axes[1][0].set_ylabel('validation')
    axes[2][0].set_ylabel('test')

    sns.despine(top=True, right=True, left=True, bottom=True)

    output_file.parent.mkdir(exist_ok=True)
    plt.savefig(output_file, bbox_inches='tight', dpi=150)

    # for category in []:
    #     tsv_file = directory / f'{category}.tsv'
    #     df = pd.read_csv(tsv_file, delimiter='\t')
    #     df = df.sort_values(by=['tracks'], ascending=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='plots number of tracks, artists and albums for train, valid and test set'
    )

    parser.add_argument('input_dir', type=Path,
                        help='stats directory from mtg-jamendo with TSV files that contains separate stats per set')
    parser.add_argument('tags_file', type=Path, help='txt file with order of tags')
    parser.add_argument('output_file', type=Path, help='figure output file')
    parser.add_argument('--category', choices=['genre', 'instrument', 'mood_theme'], default='mood_theme',
                        help='category to visualize')
    args = parser.parse_args()

    main(args.input_dir, args.tags_file, args.output_file, args.category)
