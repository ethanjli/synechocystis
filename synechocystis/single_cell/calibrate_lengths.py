#!/usr/bin/env python

import os.path
import argparse

def is_valid_file(path):
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError('{} does not exist!'.format(path))
    return path

def get_file_paths():
    parser = argparse.ArgumentParser(description='Apply length calibration to cell tracks.')
    parser.add_argument('input', type=is_valid_file,
                        help='Path of input cell tracks file (should be XLS).')
    parser.add_argument('--output', default='',
                        help=('Path of output cell tracks file (should be CSV). '
                              'If the input file ends in "in unit per min"  or '
                              '"in px per min" or "in pixels per min" before the '
                              'file extension, defaults to the input file with '
                              '"unit" or "px" or "pixels" replaced with "mm". '
                              'Otherwise, defaults to the file-extension-less input name '
                              'with the suffix " calibrated.csv".'))

    args = parser.parse_args()
    input_path = args.input
    output_path = args.output
    if not output_path:
        input_name = os.path.splitext(input_path)[0]
        if input_name.endswith('in unit per min'):
            output_path = '{}{}'.format(input_name.replace('unit', 'mm'), '.csv')
        elif input_name.endswith('in px per min'):
            output_path = '{}{}'.format(input_name.replace('px', 'mm'), '.csv')
        elif input_name.endswith('in pixels per min'):
            output_path = '{}{}'.format(input_name.replace('pixels', 'mm'), '.csv')
        else:
            output_path = '{}{}'.format(input_name, ' calibrated.csv')
    return (input_path, output_path)

def main():
    (input_path, output_path) = get_file_paths()
    print(input_path, output_path)


if __name__ == '__main__':
    main()
