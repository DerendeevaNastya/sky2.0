import math
from forSky import matrix


class SkyProgection:
    radius = 475
    center_x = 0
    center_y = 0
    half_view_angle = 90
    head_angle = 90
    distance_to_earth = 475
    rotation_angle = 0
    current_bright = 1.0
    current_percent_bright = 0


class Progection:
    def __init__(self, FormParams, constellations):
        self.form_Params = FormParams
        self.SkyProgection = SkyProgection()
        self.constellations = constellations
        for constellation in self.constellations:
            for star in constellation.stars:
                star.set_three_coordinates(self.form_Params.sky_radius)
        self.full_progection = []
        self.current_progection = []
        self.current_visual_progection = []
        self.change_earth_location_without_matrix()
        self.need_to_change_current_model = False
        self.change_sky_visual_progection()

    def set_full_progection(self):
        self.full_progection = []
        for constellation in self.constellations:
            for star in constellation.stars:
                if star.three_coordinates[0] >= 0:
                    new_star = star.dublicate_star()
                    new_star.x_progect = (
                        -new_star.three_coordinates[1] +
                        self.form_Params.sky_center_x)
                    new_star.y_progect = (
                        -new_star.three_coordinates[2] +
                        self.form_Params.sky_center_y)
                    self.full_progection.append(new_star)

    def change_sky_progect_bright_value(self, value):
        self.SkyProgection.current_percent_bright = value
        self.SkyProgection.current_bright = 1 + value * 0.055
        self.change_bright()

    def change_sky_progect_rotation_angle(self, value):
        self.SkyProgection.rotation_angle += value
        self.SkyProgection.rotation_angle %= 360

    def change_sky_progect_head_angle(self, value):
        if self.SkyProgection.head_angle + value < 0 or \
                                self.SkyProgection.head_angle + value > 180:
            return
        self.SkyProgection.head_angle -= value
        self.change_sky_progect_center_y(-value)
        self.SkyProgection.distance_to_earth = (
            self.form_Params.sky_radius *
            math.cos(math.radians(90 - self.SkyProgection.head_angle)))

    def change_sky_progect_half_view_angle(self, delta_angle):
        result = self.SkyProgection.half_view_angle - delta_angle
        if result > 90 or result < 5:
            return
        self.SkyProgection.half_view_angle -= delta_angle
        self.SkyProgection.radius = (
            self.form_Params.sky_radius *
            math.cos(math.radians(90 - self.SkyProgection.half_view_angle)))

    def change_sky_progect_center_x(self, value):
        self.SkyProgection.center_x -= value
        self.SkyProgection.center_x %= 360
        self.need_to_change_current_model = True

    def change_sky_progect_center_y(self, value):
        if math.fabs(self.SkyProgection.center_y) == 90:
            return
        if math.fabs(self.SkyProgection.center_y + value) > 90 and value != 1:
            self.SkyProgection.center_y = 90 if value > 0 else -90
            self.need_to_change_current_model = True
            return
        self.SkyProgection.center_y += value
        self.need_to_change_current_model = True

    def change_bright(self):
        self.current_visual_progection = []
        for star in self.current_progection:
            if star.apparent_magnitude <= self.SkyProgection.current_bright:
                self.current_visual_progection.append(star)

    def change_rotation(self):
        for star in self.full_progection:
            new_visual_x = (
                self.form_Params.sky_center_x +
                math.cos(math.radians(self.SkyProgection.rotation_angle)) *
                (star.x_progect - self.form_Params.sky_center_x) -
                math.sin(math.radians(self.SkyProgection.rotation_angle)) *
                (star.y_progect - self.form_Params.sky_center_y))
            new_visual_y = (
                self.form_Params.sky_center_y +
                math.sin(math.radians(self.SkyProgection.rotation_angle)) *
                (star.x_progect - self.form_Params.sky_center_x) +
                math.cos(math.radians(self.SkyProgection.rotation_angle)) *
                (star.y_progect - self.form_Params.sky_center_y))

            star.x_visual_progect = new_visual_x
            star.y_visual_progect = new_visual_y

    def change_size(self):
        self.current_progection = []
        for star in self.full_progection:
            if (self.SkyProgection.radius > (
                            (self.form_Params.sky_center_x-star.x_progect)**2 +
                            (self.form_Params.sky_center_y-star.y_progect)**2
                            )**0.5):
                self.current_progection.append(star)
        for star in self.current_progection:
            star.x_visual_progect = (
                self.form_Params.sky_center_x +
                (star.x_visual_progect -
                 self.form_Params.sky_center_x) *
                self.form_Params.sky_radius / self.SkyProgection.radius)
            star.y_visual_progect = (
                self.form_Params.sky_center_y +
                (star.y_visual_progect -
                 self.form_Params.sky_center_y) *
                self.form_Params.sky_radius / self.SkyProgection.radius)

    def change_earth_location(self):
        matrix_x = matrix.Matrix(3, 3, [[1, 0, 0],
                                        [0, 1, 0],
                                        [0, 0, 1]])
        matrix_y = matrix.Matrix(3, 3, [
            [math.cos(math.radians(self.SkyProgection.center_y)),
             0,
             math.sin(math.radians(self.SkyProgection.center_y))],
            [0, 1, 0],
            [-math.sin(math.radians(self.SkyProgection.center_y)),
             0,
             math.cos(math.radians(self.SkyProgection.center_y))]])
        matrix_z = matrix.Matrix(3, 3, [
            [math.cos(math.radians(self.SkyProgection.center_x)),
             -math.sin(math.radians(self.SkyProgection.center_x)),
             0],
            [math.sin(math.radians(self.SkyProgection.center_x)),
             math.cos(math.radians(self.SkyProgection.center_x)),
             0],
            [0, 0, 1]])
        general_matrix = matrix_x * matrix_y
        general_matrix = general_matrix * matrix_z

        for constellation in self.constellations:
            for star in constellation.stars:
                old_coordinates_matrix = matrix.Matrix(
                    3, 1, [[star.three_coordinates_default[0]],
                           [star.three_coordinates_default[1]],
                           [star.three_coordinates_default[2]]])
                new_coordinates = general_matrix * old_coordinates_matrix
                star.three_coordinates = \
                    [coord[0] for coord in new_coordinates.m]

        self.need_to_change_current_model = False
        self.set_full_progection()
        return

    def change_earth_location_without_matrix(self):
        radians_y = math.radians(self.SkyProgection.center_y)
        radians_z = math.radians(self.SkyProgection.center_x)
        cos_y = math.cos(radians_y)
        sin_y = math.sin(radians_y)
        cos_z = math.cos(radians_z)
        sin_z = math.sin(radians_z)

        for constellation in self.constellations:
            for star in constellation.stars:
                new_x = cos_y * cos_z * star.three_coordinates_default[0] - \
                        cos_y * sin_z * star.three_coordinates_default[1] + \
                        sin_y * star.three_coordinates_default[2]
                new_y = (
                    star.three_coordinates_default[0] * sin_z +
                    star.three_coordinates_default[1] * cos_z)
                new_z = (
                    -sin_y * cos_z * star.three_coordinates_default[0] +
                    sin_y * sin_z * star.three_coordinates_default[1] +
                    cos_y * star.three_coordinates_default[2])
                star.three_coordinates = [new_x, new_y, new_z]
        self.need_to_change_current_model = False
        self.set_full_progection()

    def change_sky_visual_progection(self):
        if self.need_to_change_current_model:
            self.change_earth_location_without_matrix()
        self.change_rotation()
        self.change_size()
        self.change_bright()
