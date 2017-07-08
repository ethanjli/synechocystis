#!/usr/bin/env python

import os.path
import argparse

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
plt.style.use('bmh')
plt.rcParams['font.sans-serif'] = 'Noto Sans'
plt.rcParams['mathtext.fontset'] = 'stixsans'
import pandas as pd

import util
from util import IMAGE_HEIGHT_PX, IMAGE_WIDTH_PX
from util import length_name, time_name, speed_name
from util import displacement_component_name, velocity_component_name
from util import convert_length

LENGTH_UNIT = 'mm'
TIME_UNIT = 'min'

def get_parameters():
    parser = argparse.ArgumentParser(description='Apply length calibration to cell tracks.')
    parser.add_argument('input', type=util.is_valid_file,
                        help='Path of input calibrated cell tracks file (should be CSV).')
    parser.add_argument('--output', default='',
                        help=('Path of output plot files (should be extensionless). '
                              'Defaults to the file-extension-less input name '
                              'with various suffixes.'))
    parser.add_argument('--format', default='pdf',
                        help='Filetype of output plot files. Defaults to "pdf".')

    args = parser.parse_args()
    input_path = args.input
    output_path = args.output
    file_format = args.format
    if not output_path:
        output_path = os.path.splitext(input_path)[0]
    return (input_path, output_path, file_format)

def process_input(input_path):
    # Read the tracks
    df = pd.read_csv(input_path)

    return df

def generate_plots(df, output_path, file_format):
    image_max_length = convert_length(max(IMAGE_HEIGHT_PX, IMAGE_WIDTH_PX),
                                      'px', LENGTH_UNIT)

    # Directional displacements histogram
    plt.figure()
    columns = [
        displacement_component_name('x', LENGTH_UNIT),
        displacement_component_name('y', LENGTH_UNIT)
    ]
    ax = df.loc[:, columns].plot.hist(
        alpha=0.5, xlim=[-image_max_length, image_max_length],
        title=r'$x-$ and $y-$ Displacements', figsize=(8, 6)
    )
    ax.legend(['x', 'y'])
    ax.set_xlabel('Displacement (mm)')
    plt.savefig(output_path + ' displacements.' + file_format, format=file_format)

    # Distance vs. direction polar scatterplot
    columns = [
        'direction_deg',
        length_name('distance', LENGTH_UNIT)
    ]
    fig = plt.figure(figsize=(8, 8))
    plt.polar(df[columns[0]].dropna(), df[columns[1]].dropna(), 'o')
    ax = fig.axes[0]
    ax.set_xlabel(r'Direction ($^\circ$)')
    ax.set_ylim(0, image_max_length)
    ax.set_ylabel('Displacement (mm)')
    ax.set_rlabel_position(90)
    plt.savefig(output_path + ' distancespolar.' + file_format, format=file_format)

    # Distances histogram
    plt.figure()
    ax = df[length_name('distance', LENGTH_UNIT)].plot.hist(
        xlim=[-image_max_length, image_max_length],
        title='Net Distances', figsize=(8, 6)
    )
    ax.set_xlabel('Distance (mm)')
    plt.savefig(output_path + ' distances.' + file_format, format=file_format)

def main():
    (input_path, output_path, file_format) = get_parameters()
    df = process_input(input_path)
    generate_plots(df, output_path, file_format)


if __name__ == '__main__':
    main()
