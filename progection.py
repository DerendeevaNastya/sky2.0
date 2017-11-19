import math
import copy
import stars_data
import matrix


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
    displacement_vector = [0, 0]


class Progection:
    def __init__(self, FormParams, constellations):
        self.form_Params = FormParams
        self.constellations = constellations
        self.current_model = []
        self.change_earth_location()
        self.need_to_change_current_model = False  # полная проекция на плоскость на 180`
        self.full_progection = []                  # сужение на half_view_angle
        self.current_progection = []               # изменение количества по яркости
        self.current_visual_progection = []
        self.set_full_progection()
        self.change_sky_visual_progection()

    def set_full_progection(self):
        self.full_progection = []
        for star in self.current_model:
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
        SkyProgection.current_percent_bright = value
        SkyProgection.current_bright = 1 + value * 0.055
        self.change_bright()

    def change_sky_progect_rotation_angle(self, value):
        SkyProgection.rotation_angle += value
        SkyProgection.rotation_angle %= 360

    def change_sky_progect_head_angle(self, value):
        if SkyProgection.head_angle + value < 0 or \
                                SkyProgection.head_angle + value > 180:
            return
        SkyProgection.head_angle -= value
        self.change_sky_progect_center_y(-value)
        SkyProgection.distance_to_earth = (
            self.form_Params.sky_radius *
            math.cos(math.radians(90 - SkyProgection.head_angle)))

    def change_sky_progect_half_view_angle(self, delta_angle):
        if (
                            SkyProgection.half_view_angle - delta_angle > 90 or
                            SkyProgection.half_view_angle - delta_angle < 5):
            return
        SkyProgection.half_view_angle -= delta_angle
        SkyProgection.radius = (
            self.form_Params.sky_radius *
            math.cos(math.radians(90 - SkyProgection.half_view_angle)))

    def change_sky_progect_center_x(self, value):
        SkyProgection.center_x += value
        SkyProgection.center_x %= 360
        self.need_to_change_current_model = True

    def change_sky_progect_center_y(self, value):
        if math.fabs(SkyProgection.center_y) == 90:
            return
        SkyProgection.center_y += value
        self.need_to_change_current_model = True

    def change_bright(self):
        self.current_visual_progection = []
        for star in self.current_progection:
            if star.apparent_magnitude <= SkyProgection.current_bright:
                self.current_visual_progection.append(star)

    def change_rotation(self):
        for star in self.full_progection:
            new_visual_x = (
                self.form_Params.sky_center_x +
                math.cos(math.radians(SkyProgection.rotation_angle)) *
                (star.x_progect - self.form_Params.sky_center_x) -
                math.sin(math.radians(SkyProgection.rotation_angle)) *
                (star.y_progect - self.form_Params.sky_center_y))
            new_visual_y = (
                self.form_Params.sky_center_y +
                math.sin(math.radians(SkyProgection.rotation_angle)) *
                (star.x_progect - self.form_Params.sky_center_x) +
                math.cos(math.radians(SkyProgection.rotation_angle)) *
                (star.y_progect - self.form_Params.sky_center_y))

            star.x_visual_progect = new_visual_x
            star.y_visual_progect = new_visual_y

    def change_size(self):
        self.current_progection = []
        for star in self.full_progection:
            if (SkyProgection.radius > (
                            (self.form_Params.sky_center_x-star.x_progect)**2 +
                            (self.form_Params.sky_center_y-star.y_progect)**2
                            )**0.5):
                self.current_progection.append(star)
        for star in self.current_progection:
            star.x_visual_progect = (
                self.form_Params.sky_center_x +
                (star.x_visual_progect -
                 self.form_Params.sky_center_x) *
                self.form_Params.sky_radius / SkyProgection.radius)
            star.y_visual_progect = (
                self.form_Params.sky_center_y +
                (star.y_visual_progect -
                 self.form_Params.sky_center_y) *
                self.form_Params.sky_radius / SkyProgection.radius)

    def change_earth_location(self):
        self.current_model = []
        for constellation in self.constellations:
            for star in constellation.stars:
                star.set_three_coordinates(self.form_Params.sky_radius)

        matrix_x = matrix.Matrix(3, 3, [[1, 0, 0],
                                        [0, 1, 0],
                                        [0, 0, 1]])
        matrix_y = matrix.Matrix(3, 3, [
            [math.cos(math.radians(SkyProgection.center_y)),
             0,
             math.sin(math.radians(SkyProgection.center_y))],
            [0, 1, 0],
            [-math.sin(math.radians(SkyProgection.center_y)),
             0,
             math.cos(math.radians(SkyProgection.center_y))]])
        matrix_z = matrix.Matrix(3, 3, [
            [math.cos(math.radians(SkyProgection.center_x)),
             -math.sin(math.radians(SkyProgection.center_x)),
             0],
            [math.sin(math.radians(SkyProgection.center_x)),
             math.cos(math.radians(SkyProgection.center_x)),
             0],
            [0, 0, 1]])
        general_matrix = matrix_x * matrix_y
        general_matrix = general_matrix * matrix_z

        for constellation in self.constellations:
            for star in constellation.stars:
                new_star = copy.deepcopy(star)
                old_coordinates_matrix = matrix.Matrix(
                    3, 1, [[star.three_coordinates[0]],
                           [star.three_coordinates[1]],
                           [star.three_coordinates[2]]])
                new_coordinates = general_matrix * old_coordinates_matrix
                new_star.three_coordinates = \
                    [coord[0] for coord in new_coordinates.m]
                self.current_model.append(new_star)
        self.need_to_change_current_model = False
        self.set_full_progection()
        return

    def change_sky_visual_progection(self):
        if self.need_to_change_current_model:
            self.change_earth_location()
        self.change_rotation()
        self.change_size()
        self.change_bright()
