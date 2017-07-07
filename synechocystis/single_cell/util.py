#!/usr/bin/env python

import os.path
import argparse

IMAGE_HEIGHT_PX = 720
IMAGE_WIDTH_PX = 960

# NAMING
def length_name(name, unit):
    return '{}_{}'.format(name, unit)

def time_name(name, unit):
    return '{}_{}'.format(name, unit)

def speed_name(name, length_unit, time_unit):
    return '{}_{}/{}'.format(name, length_unit, time_unit)

def displacement_component_name(name, unit):
    return '{}_displacement_{}'.format(name, unit)

def velocity_component_name(name, length_unit, time_unit):
    return '{}_velocity_{}/{}'.format(name, length_unit, time_unit)


# UNITS

CONVERSIONS = {
    'px': {
        'px': 1.0,
        'mm': 1.0 / 4440
    },
    'min': {
        'min': 1.0,
        's': 60.0
    }
}

def convert_length(value, length_unit, to_length_unit):
    length_conversion = CONVERSIONS[length_unit][to_length_unit]
    return value * length_conversion

def convert_time(value, time_unit, to_time_unit):
    time_conversion = CONVERSIONS[time_unit][to_time_unit]
    return value * time_conversion

def convert_speed(value, length_unit, time_unit, to_length_unit, to_time_unit):
    length_conversion = CONVERSIONS[length_unit][to_length_unit]
    time_conversion = CONVERSIONS[time_unit][to_time_unit]
    return value * length_conversion / time_conversion

# FILE OPERATIONS

def is_valid_file(path):
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError('{} does not exist!'.format(path))
    return path

