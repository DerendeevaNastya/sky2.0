from forSky import stars_data


# для вычисления угла используется модифицированная формула
# определения времени по звездам
def get_center_x_from_time_sec(local_datetime):
    new_star = stars_data.Star('', 0, '11:3:43.7', '+00:00:00',
                               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    old_angle_sec = new_star.x_sec
    local_time = local_datetime.hour + local_datetime.minute / 60
    new_hour = (((55.3 - local_time) / 2) -
                (local_datetime.day / 30) -
                local_datetime.month)
    new_hour = new_hour - 12 if new_hour > 12 else new_hour
    new_angle_sec = new_hour * 3600
    return new_angle_sec * 30 - old_angle_sec


# корректирует положение звезды в зависимости от её n_alf и n_del
def change_constellation_from_year(local_datetime, constellations):
    koeff = local_datetime.year - 2000
    for constellation in constellations:
        for star in constellation.stars:
            star.x_sec += koeff * star.n_alf
            star.y_sec += koeff * star.n_del
    return constellations
