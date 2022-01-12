import argparse
import csv
import itertools
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib import rcParams


def main(input_file: Path, tags_file: Path, output_file: Path, keep_prefix: bool, relative: bool) -> None:
    tags = np.loadtxt(str(tags_file), dtype=str)
    n = len(tags)
    tags_indices = {tag: i for i, tag in enumerate(tags)}
    matrix = np.zeros(shape=(n, n))

    with input_file.open() as fp:
        reader = csv.reader(fp, delimiter='\t')
        next(reader, None)  # skip header
        for row in reader:
            track_tags = row[5:]
            for tag in track_tags:
                idx = tags_indices[tag]
                matrix[idx, idx] += 1
            for tag1, tag2 in itertools.combinations(track_tags, 2):
                idx1 = tags_indices[tag1]
                idx2 = tags_indices[tag2]
                matrix[idx1, idx2] += 1
                matrix[idx2, idx1] += 1

    if relative:
        matrix /= matrix.diagonal()
        to_str = np.vectorize(lambda x: f'{x:.1f}'.removeprefix('0') if 0.2 <= x < 1.0 else ' ')
    else:
        to_str = np.vectorize(lambda x: str(int(x)) if 50 <= x else ' ')
    annotations = to_str(matrix)

    plt.figure(figsize=(19, 15))
    rcParams['font.family'] = 'serif'
    rcParams['font.serif'] = 'Times New Roman'

    labels = [tag.split('---')[1] for tag in tags] if not keep_prefix else tags
    sns.heatmap(matrix, cmap='mako_r', xticklabels=labels, yticklabels=labels, annot=annotations, fmt='s')

    plt.tick_params(left=False, bottom=False)

    output_file.parent.mkdir(exist_ok=True)
    plt.savefig(output_file, bbox_inches='tight', dpi=150)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Plots the co-occurrence matrix of tags')
    parser.add_argument('tsv_file', type=Path, help='input TSV file with list of tracks and tags')
    parser.add_argument('tags_file', type=Path, help='input TXT file with list of tags')
    parser.add_argument('output_file', type=Path, help='figure output file')
    parser.add_argument('--keep-prefix', action='store_true', help='keep "category---" prefix from figure')
    parser.add_argument('--relative', action='store_true', help='represent co-occurrences as ratios')
    args = parser.parse_args()

    main(args.tsv_file, args.tags_file, args.output_file, args.keep_prefix, args.relative)
