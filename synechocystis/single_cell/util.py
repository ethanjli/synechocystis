#!/usr/bin/env python

import os.path
import argparse

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

# FILE OPERATIONS

def is_valid_file(path):
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError('{} does not exist!'.format(path))
    return path

