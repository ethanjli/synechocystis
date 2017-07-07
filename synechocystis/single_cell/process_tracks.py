#!/usr/bin/env python

import os.path
import argparse

import numpy as np
import pandas as pd

import util
from util import length_name, time_name, speed_name
from util import displacement_component_name, velocity_component_name
from util import convert_length, convert_time, convert_speed

OUTPUT_LENGTH_UNIT = 'mm'
OUTPUT_TIME_UNIT = 'min'

def get_parameters():
    parser = argparse.ArgumentParser(description='Process cell tracks.')
    parser.add_argument('input', type=util.is_valid_file,
                        help='Path of input cell tracks file (should be CSV).')
    parser.add_argument('--output', default='',
                        help=('Path of output cell tracks file (should be CSV). '
                              'If the input file ends in "in unit per min"  or '
                              '"in px per min" or "in pixels per min" before the '
                              'file extension, defaults to the input file with '
                              '"unit" or "px" or "pixels" replaced with "mm". '
                              'Otherwise, defaults to the file-extension-less input name '
                              'with the suffix " processed.csv".'))
    parser.add_argument('--length_unit', default='px',
                        help='Units of length in input cell tracks file.')
    parser.add_argument('--time_unit', default='min',
                        help='Units of time in input cell tracks file.')

    args = parser.parse_args()
    input_path = args.input
    output_path = args.output
    length_unit = args.length_unit
    time_unit = args.time_unit
    if not output_path:
        input_name = os.path.splitext(input_path)[0]
        if input_name.endswith('in unit per min'):
            output_path = '{}{}'.format(input_name.replace('unit', 'mm'), '.csv')
        elif input_name.endswith('in px per min'):
            output_path = '{}{}'.format(input_name.replace('px', 'mm'), '.csv')
        elif input_name.endswith('in pixels per min'):
            output_path = '{}{}'.format(input_name.replace('pixels', 'mm'), '.csv')
        else:
            output_path = '{}{}'.format(input_name, ' processed.csv')
    return (input_path, output_path, length_unit, time_unit)

def process_input(input_path, length_unit, time_unit):
    # Read the tracks
    df = pd.read_csv(input_path, header=0, sep='\t',
                     names=['track', 'slice',
                            length_name('x', length_unit),
                            length_name('y', length_unit),
                            length_name('distance', length_unit),
                            speed_name('speed', length_unit, time_unit),
                            'value'],
                     na_values={
                         length_name('distance', length_unit): -1.0,
                         speed_name('speed', length_unit, time_unit): -1.0
                     })

    # Add time column
    df[time_name('duration', time_unit)] = (
        df[length_name('distance', length_unit)] /
        df[speed_name('speed', length_unit, time_unit)]
    )

    # Add unit conversion columns
    for column in ['x', 'y', 'distance']:
        col_in = df[length_name(column, length_unit)]
        if column == 'y' and OUTPUT_LENGTH_UNIT != 'px':
            col_out = convert_length(util.IMAGE_HEIGHT_PX - col_in,
                                     length_unit, OUTPUT_LENGTH_UNIT)
        else:
            col_out = convert_length(col_in, length_unit, OUTPUT_LENGTH_UNIT)
        df[length_name(column, OUTPUT_LENGTH_UNIT)] = col_out
    for column in ['duration']:
        col_in = df[time_name(column, time_unit)]
        col_out = convert_time(col_in, time_unit, OUTPUT_TIME_UNIT)
        df[time_name(column, OUTPUT_TIME_UNIT)] = col_out
    for column in ['speed']:
        col_in = df[speed_name(column, length_unit, time_unit)]
        col_out = convert_speed(col_in, length_unit, time_unit,
                                OUTPUT_LENGTH_UNIT, OUTPUT_TIME_UNIT)
        df[speed_name(column, OUTPUT_LENGTH_UNIT, OUTPUT_TIME_UNIT)] = col_out

    return df

def calculate_metrics(df):
    # Calculate x and y components of distance and speed
    durations = df[time_name('duration', OUTPUT_TIME_UNIT)]
    for column in ['x', 'y']:
        # Distance
        col_in = df[length_name(column, OUTPUT_LENGTH_UNIT)]
        col_out = col_in.diff()
        col_out[pd.isnull(durations)] = np.nan
        df[displacement_component_name(column, OUTPUT_LENGTH_UNIT)] = col_out
        # Speed
        df[velocity_component_name(
            column, OUTPUT_LENGTH_UNIT, OUTPUT_TIME_UNIT
        )] = col_out / durations

    # Calculate direction of motion
    x_displacement = df[displacement_component_name('x', OUTPUT_LENGTH_UNIT)]
    y_displacement = df[displacement_component_name('y', OUTPUT_LENGTH_UNIT)]
    direction = np.arctan2(y_displacement, x_displacement)
    df['direction_rad'] = direction
    df['direction_deg'] = np.rad2deg(direction)

    return df

def main():
    (input_path, output_path, length_unit, time_unit) = get_parameters()
    df = process_input(input_path, length_unit, time_unit)
    df = calculate_metrics(df)
    df.to_csv(output_path, index=False)


if __name__ == '__main__':
    main()
