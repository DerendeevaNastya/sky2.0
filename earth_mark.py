#!/usr/bin/env python3

import stars_data

def create_earth_mark(center_x, center_y):
    earth_mark = stars_data.Constellation('earth_mark')
    mark = stars_data.Star('earth mark', 0, '00:00:00', '+00:00:00', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    mark.x_sec = center_x * 3600
    mark.y_sec = (center_y - 90) * 3600
    earth_mark.stars = [mark]
    return earth_mark