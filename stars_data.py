from os import listdir, path
import copy
import math

DATA_BASE = './stars/txt/'

class Star:
    def __init__(self, constellation_name, map_number, location_x, location_y,
                 l, b, T, apparent_magnitude, spectral_class,
                 n_alf, n_del, p, vr, HD, Fl_Ba):
        self.constellation_name = constellation_name
        self.map_number = int(map_number)
        self.x_str = location_x
        self.y_str = location_y

        self.x_sec = 0
        self.y_sec = 0
        self.get_location_x()
        self.get_location_y()

        self.x_progect = 0
        self.y_progect = 0
        self.x_visual_progect = 0
        self.y_visual_progect = 0

        self.three_coordinates = []

        self.l = l
        self.b = b
        self.T = T
        self.apparent_magnitude = float(apparent_magnitude)
        self.spectral_class = spectral_class
        self.n_alf = float(n_alf)
        self.n_del = float(n_del)
        self.p = p
        self.vr = vr
        self.HD = HD
        self.Fl_Ba = Fl_Ba

    def dublicate_star(self):
        return copy.deepcopy(self)

    def get_location_x(self):
        count = 0
        koeff = [3600, 60, 1]
        numbers = [float(x) for x in self.x_str.split(':')]
        for i in range(0, 3):
            count += koeff[i] * numbers[i]
        count = count * 15
        self.x_sec = count

    def get_location_y(self):
        self.y_sec = 0
        sign = -1 if self.y_str[0] == '-' else 1
        koeff = [3600, 60, 1]
        numbers = [int(x) for x in self.y_str[1:].split(':')]
        for i in range(0, 3):
            self.y_sec += koeff[i] * numbers[i]
        self.y_sec *= sign

    def set_three_coordinates(self, radius):
        x = radius * math.sin(math.radians(90 - self.y_sec / 3600)) * math.cos(math.radians(self.x_sec / 3600))
        y = radius * math.sin(math.radians(90 - self.y_sec / 3600)) * math.sin(math.radians(self.x_sec / 3600))
        z = radius * math.cos(math.radians(90 - self.y_sec / 3600))
        self.three_coordinates = [x, y, z]

    def get_information(self):
        information = 'constellation: ' + self.constellation_name + '\n'
        information += 'location: ' + self.x_str + ' ' + self.y_str + '\n'
        information += 'apparent magnitude: ' + str(self.apparent_magnitude) + '\n'
        information += 'spectral class: ' + str(self.spectral_class)
        return information


class Constellation:
    def __init__(self, name):
        self.name = name
        self.stars = []


def get_constellations():
    files = listdir(DATA_BASE)
    constellation_list = []
    lines_data = [3, 11, 10, 7, 7, 3, 5, 21, 7, 7, 6, 5, 7, 7]
    for file in files:
        with open(DATA_BASE + file) as f:
            new_constellation = Constellation(path.splitext(file)[0])
            for star_data in f:
                star_data_list = [new_constellation.name]
                for i in lines_data:
                    data_part = star_data[:i]
                    star_data_list.append(''.join(data_part.split()))
                    star_data = star_data[i:]
                new_constellation.stars.append(Star(*star_data_list))
        constellation_list.append(new_constellation)
    return constellation_list
