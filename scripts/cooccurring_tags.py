import argparse
import csv
import itertools
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def main(input_file: Path, tags_file: Path, output_file: Path, remove_prefix: bool) -> None:
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

    plt.figure(figsize=(15, 15))
    labels = [tag.split('---')[1] for tag in tags] if remove_prefix else tags
    sns.heatmap(matrix, cmap='mako_r', xticklabels=labels, yticklabels=labels, square=True)
    plt.savefig(output_file, bbox_inches='tight')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Plots the co-occurrence matrix of tags')
    parser.add_argument('tsv_file', type=Path, help='Input TSV file with list of tracks and tags')
    parser.add_argument('tags_file', type=Path, help='Input TSV file with list of tracks and tags')
    parser.add_argument('output_file', type=Path, help='Figure output file')
    parser.add_argument('--remove-prefix', action='store_true', help='Remove --- prefix from figure')
    args = parser.parse_args()

    main(args.tsv_file, args.tags_file, args.output_file, args.remove_prefix)
