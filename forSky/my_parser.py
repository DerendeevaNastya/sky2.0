#!/usr/bin/env python3
import argparse
import datetime

import math


def create_parser():
    parser = argparse.ArgumentParser(description='sky')
    parser.add_argument('-datetime', type=str, default=datetime.datetime.now(),
                        nargs='+',
                        help="local date (default=now) "
                             "format: YYYY-mm-dd hh:mm:ss")
    parser.add_argument('-lat', dest='lat', type=int, nargs='?', default=0,
                        help="watcher's latitude (default=0) "
                             "-90<=latitude<=90")
    parser.add_argument('-long', dest='long', type=int, nargs='?', default=0,
                        help="watcher's longtitude (default=0) "
                             "0<=longtitude<=359 (for example: 30' west lat = -30, 30' east lat = 30)")
    return parser


def get_correct_namespace():
    parser = create_parser()
    namespace = parser.parse_args()
    check_data(namespace)
    return namespace


def check_data(namespace):
    if math.fabs(namespace.lat) > 90:
        raise Exception('latitude must be in [-90, 90]')
    if namespace.long > 359 or namespace.long < 0:
        raise Exception('longtitude must be in [0, 360]')
    try:
        if type(namespace.datetime) is list:
            namespace.datetime = datetime.datetime.strptime(
                ' '.join(namespace.datetime), "%Y-%m-%d %H:%M:%S")
    except Exception:
        raise Exception('incorrect datetime')
