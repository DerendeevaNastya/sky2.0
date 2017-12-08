from forSky import stars_data


def create_latitudes_and_longtitudes():
    all_lines = []
    for i in range(-80, 81, 10):
        latitude = stars_data.Constellation('latitude' + str(i))
        points = []
        for x in range(0, 361, 3):
            new_point = stars_data.Star('latitude' + str(i), 0,
                                        '00:00:00', '+00:00:00',
                                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            new_point.x_sec = x * 3600
            new_point.y_sec = i * 3600
            points.append(new_point)
            latitude.stars = points
        all_lines.append(latitude)

    for i in range(0, 360, 10):
        longtitude = stars_data.Constellation('longtitude' + str(i))
        points = []
        for y in range(-90, 91, 3):
            new_point = stars_data.Star('longtitude' + str(i), 0,
                                        '00:00:00', '+00:00:00',
                                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            new_point.x_sec = i * 3600
            new_point.y_sec = y * 3600
            points.append(new_point)
            longtitude.stars = points
        all_lines.append(longtitude)

    return all_lines


def create_earth_mark(center_x, center_y):
    earth_mark = stars_data.Constellation('earth_mark')
    mark = stars_data.Star('earth mark', 0, '00:00:00', '+00:00:00',
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    mark.x_sec = center_x * 3600
    mark.y_sec = (center_y - 90) * 3600
    earth_mark.stars = [mark]
    return earth_mark
