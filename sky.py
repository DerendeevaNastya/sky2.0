import math
import sys
import stars_data
import progection
import grid
import copy
from itertools import groupby
from PyQt5.QtCore import QPoint, Qt, QSize, QUrl
from PyQt5.QtGui import QPainter, QColor, QFont, QIcon, QImage, QPolygon
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QSlider
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


COLORS = {'O': QColor(102, 253, 255),
          'B': QColor(153, 204, 255),
          'A': QColor(210, 255, 255),
          'F': QColor(255, 255, 255),
          'G': QColor(255, 247, 127),
          'K': QColor(255, 232, 79),
          'M': QColor(255, 157, 45)}


class FormParams:
    form_x = 1300
    form_y = 1000
    dx = 300
    dy = 0
    sky_radius = 475
    sky_center_x = 800
    sky_center_y = 500


class Sky(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 40, FormParams.form_x, FormParams.form_y)
        self.setWindowTitle('Sky')
        self.progection = progection.Progection(
            FormParams, stars_data.get_constellations())
        self.grid = progection.Progection(
            FormParams, grid.create_latitudes_and_longtitudes())
        self.turn_on_grid = True
        self.print_inf = False
        self.star_for_inf = None
        self.create_bottoms()
        self.create_bright_slider()
        self.create_media_player()
        self.show()

    def create_media_player(self):
        self.player = QMediaPlayer()
        self.player.setMedia(
            QMediaContent(QUrl.fromLocalFile('music/cosmic.mp3')), None)
        self.player.setVolume(30)
        self.player.play()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setBrush(Qt.black)
        qp.drawRect(self.rect())
        self.draw_sky(qp)
        if self.print_inf:
            self.print_information(qp, self.star_for_inf)
        qp.end()

    def wheelEvent(self, QWheelEvent):
        point = QWheelEvent.angleDelta()
        self.progection.change_sky_progect_half_view_angle(point.y() / 24)
        self.progection.change_sky_visual_progection()
        self.grid.change_sky_visual_progection()
        self.repaint()

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_A:
            self.progection.change_sky_progect_rotation_angle(-1)
            self.progection.change_sky_visual_progection()
            self.grid.change_sky_visual_progection()
            self.repaint()
        if key == Qt.Key_D:
            self.progection.change_sky_progect_rotation_angle(1)
            self.progection.change_sky_visual_progection()
            self.grid.change_sky_visual_progection()
            self.repaint()
        if key == Qt.Key_W:
            self.progection.change_sky_progect_head_angle(-1)
            self.grid.need_to_change_current_model = True
            self.grid.change_sky_visual_progection()
            self.progection.change_sky_visual_progection()
            self.repaint()
        if key == Qt.Key_S:
            self.progection.change_sky_progect_head_angle(1)
            self.grid.need_to_change_current_model = True
            self.progection.change_sky_visual_progection()
            self.grid.change_sky_visual_progection()
            self.repaint()

        if key == Qt.Key_3:
            self.progection.change_sky_progect_center_x(1)
            self.progection.change_sky_visual_progection()
            self.grid.need_to_change_current_model = True
            self.grid.change_sky_visual_progection()
            self.repaint()
        if key == Qt.Key_1:
            self.progection.change_sky_progect_center_x(-1)
            self.progection.change_sky_visual_progection()
            self.grid.need_to_change_current_model = True
            self.grid.change_sky_visual_progection()
            self.repaint()
        if key == Qt.Key_5:
            self.progection.change_sky_progect_center_y(1)
            self.progection.change_sky_visual_progection()
            self.grid.need_to_change_current_model = True
            self.grid.change_sky_visual_progection()
            self.repaint()
        if key == Qt.Key_2:
            self.progection.change_sky_progect_center_y(-1)
            self.progection.change_sky_visual_progection()
            self.grid.need_to_change_current_model = True
            self.grid.change_sky_visual_progection()
            self.repaint()

    def print_nearest_star_information(self, mouse_x, mouse_y):
        stars = {}
        for star in self.progection.current_visual_progection:
            distance = math.sqrt(math.pow(mouse_x - star.x_visual_progect, 2) +
                                 math.pow(mouse_y - star.y_visual_progect, 2))
            if distance <= 10:
                stars[star] = distance

        if len(stars) == 0:
            self.print_inf = False
            self.star_for_inf = None
            self.repaint()
            return
        nearest_star = None
        min_distance = 10
        for star in stars:
            if stars[star] < min_distance:
                min_distance = stars[star]
                nearest_star = star
        self.star_for_inf = nearest_star
        self.print_inf = True
        self.repaint()

    def mousePressEvent(self, QMouseEvent):
        self.print_nearest_star_information(QMouseEvent.x(), QMouseEvent.y())

    def print_information(self, qp, star):
        if star is None:
            return
        star_information = star.get_information()
        star_information += ('\n' + 'x: ' + str(star.three_coordinates[0]) +
                             '\ny: ' + str(star.three_coordinates[1]) +
                             '\nz: ' + str(star.three_coordinates[2]))
        qp.setPen(QColor(200, 200, 200))
        qp.setFont(QFont('Decorative', 10))
        qp.drawText(0, 600, FormParams.dx, FormParams.form_y,
                    Qt.AlignLeft, star_information)

    def change_size_max(self):
        self.progection.change_sky_progect_half_view_angle(5)
        self.progection.change_sky_visual_progection()
        self.grid.need_to_change_current_model = True
        self.grid.change_sky_visual_progection()
        self.repaint()

    def change_size_min(self):
        self.progection.change_sky_progect_half_view_angle(-5)
        self.progection.change_sky_visual_progection()
        self.grid.need_to_change_current_model = True
        self.grid.change_sky_visual_progection()
        self.repaint()

    def change_clock_rotation(self, angle):
        self.progection.change_sky_progect_rotation_angle(5)
        self.progection.change_sky_visual_progection()
        self.grid.need_to_change_current_model = True
        self.grid.change_sky_visual_progection()
        self.repaint()

    def change_unclock_rotation(self, angle):
        self.progection.change_sky_progect_rotation_angle(-5)
        self.progection.change_sky_visual_progection()
        self.grid.need_to_change_current_model = True
        self.grid.change_sky_visual_progection()
        self.repaint()

    def change_bright(self, value):
        self.progection.change_sky_progect_bright_value(value)
        self.progection.change_sky_visual_progection()
        self.repaint()

    def turn_on_off_grid(self):
        self.turn_on_grid = not self.turn_on_grid
        self.repaint()

    def create_bright_slider(self):
        sld = QSlider(Qt.Vertical, self)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setGeometry(100, 350, 30, 110)
        sld.valueChanged[int].connect(self.change_bright)
        sld.show()

    def create_bottoms(self):
        btn_clock_rotation = QPushButton(self)
        btn_clock_rotation.setToolTip('clockwise rotate')
        btn_clock_rotation.resize(48, 48)
        btn_clock_rotation.clicked.connect(self.change_clock_rotation)
        btn_clock_rotation.setIcon(QIcon('images/rotate_right1600.png'))
        btn_clock_rotation.setIconSize(QSize(47, 47))
        btn_clock_rotation.move(100, 50)
        btn_clock_rotation.show()

        btn_unclock_rotation = QPushButton(self)
        btn_unclock_rotation.setToolTip('counterclockwise rotate')
        btn_unclock_rotation.resize(48, 48)
        btn_unclock_rotation.clicked.connect(self.change_unclock_rotation)
        btn_unclock_rotation.setIcon(QIcon('images/rotate_left1600.png'))
        btn_unclock_rotation.setIconSize(QSize(46, 46))
        btn_unclock_rotation.move(50, 50)
        btn_unclock_rotation.show()

        btn_max = QPushButton(self)
        btn_max.resize(48, 48)
        btn_max.clicked.connect(self.change_size_max)
        btn_max.setIcon(QIcon('images/plus.png'))
        btn_max.setIconSize(QSize(47, 47))
        btn_max.move(200, 50)
        btn_max.show()

        btn_min = QPushButton(self)
        btn_min.resize(48, 48)
        btn_min.clicked.connect(self.change_size_min)
        btn_min.setIcon(QIcon('images/minus.png'))
        btn_min.setIconSize(QSize(47, 47))
        btn_min.move(200, 100)
        btn_min.show()

        btn_grid = QPushButton(self)
        btn_grid.resize(48, 48)
        btn_grid.setToolTip('on/off grid')
        btn_grid.clicked.connect(self.turn_on_off_grid)
        btn_grid.setIcon(QIcon('images/worldgrid.png'))
        btn_grid.setIconSize(QSize(47, 47))
        btn_grid.move(200, 300)
        btn_grid.setStyleSheet("""
            QPushButton:hover { background-color: black }
            QPushButton:!hover { background-color: black }
            QPushButton:pressed { background-color: black }
        """)
        btn_grid.show()

    def draw_layout(self, qp):
        qp.setPen(QColor(200, 200, 200))
        qp.drawLine(
            QPoint(FormParams.dx - 1, 0),
            QPoint(FormParams.dx - 1, FormParams.form_y))
        qp.setPen(QColor(86, 86, 86))
        qp.drawEllipse(FormParams.sky_center_x - FormParams.sky_radius,
                       FormParams.sky_center_y - FormParams.sky_radius,
                       FormParams.sky_radius * 2,
                       FormParams.sky_radius * 2)

    def draw_black_frame(self, qp):
        image = QImage('images/рамка.png')
        qp.drawImage(QPoint(FormParams.dx - 1, -2), image)

    def draw_earth(self, qp):
        poligon = []
        if progection.SkyProgection.head_angle <= 90:
            poligon = QPolygon([QPoint(FormParams.dx, FormParams.form_y),
                                QPoint(FormParams.form_x, FormParams.form_y),
                                QPoint(FormParams.form_x,
                                       -(progection.SkyProgection.radius - progection.SkyProgection.distance_to_earth) + FormParams.sky_center_y + FormParams.sky_radius),
                                QPoint(FormParams.dx, -(progection.SkyProgection.radius - progection.SkyProgection.distance_to_earth)
                                  + FormParams.sky_center_y + FormParams.sky_radius)])
        else:
            poligon = QPolygon([QPoint(FormParams.dx, 0),
                            QPoint(FormParams.form_x, 0),
                            QPoint(FormParams.form_x,
                                   (progection.SkyProgection.radius - progection.SkyProgection.distance_to_earth)
                                   + FormParams.sky_center_y - FormParams.sky_radius),
                            QPoint(FormParams.dx,
                                   (progection.SkyProgection.radius - progection.SkyProgection.distance_to_earth)
                                   + FormParams.sky_center_y - FormParams.sky_radius)])
        qp.setPen(QColor(14, 41, 75))
        qp.setBrush(QColor(14, 41, 75))
        qp.drawPolygon(poligon)

    def draw_grid(self, qp):
        qp.setPen(QColor(14, 41, 75))
        if not self.turn_on_grid:
            return
        for g in groupby(sorted(self.grid.current_visual_progection,
                                key=lambda x: x.constellation_name),
                         key=lambda x: x.constellation_name):
            old_point = None
            points = list(g[1])
            for point in points:
                if old_point is not None and \
                                math.fabs(old_point.x_sec - point.x_sec) / 3600 <= 5 and \
                                math.fabs(old_point.y_sec - point.y_sec) / 3600 <= 5:
                    qp.drawLine(old_point.x_visual_progect,
                                old_point.y_visual_progect,
                                point.x_visual_progect,
                                point.y_visual_progect)
                old_point = point

    def draw_backlight(self, qp):
        for star in self.progection.current_visual_progection:
            if (self.star_for_inf is not None and
                    star.constellation_name == self.star_for_inf.constellation_name):
                qp.setBrush(QColor(0, 30, 30))
                qp.setPen(QColor(0, 30, 30))
                qp.drawEllipse(star.x_visual_progect - 10,
                               star.y_visual_progect - 10,
                               20, 20)

        for star in self.progection.current_visual_progection:
            if self.star_for_inf is not None and \
                            self.star_for_inf.x_str == star.x_str and \
                            self.star_for_inf.y_str == star.y_str:
                qp.setBrush(QColor(100, 175, 183))
                qp.setPen(QColor(100, 175, 183))
                qp.drawEllipse(star.x_visual_progect - 8,
                               star.y_visual_progect - 8,
                               15, 15)

    def draw_progection(self, qp):
        for star in self.progection.current_visual_progection:
            star_size = 1
            if star.apparent_magnitude <= 1:
                star_size = 6
            elif star.apparent_magnitude <= 2:
                star_size = 4
            elif star.apparent_magnitude <= 4:
                star_size = 3
            elif star.apparent_magnitude <= 5:
                star_size = 2

            qp.setBrush(QColor(250, 250, 250))
            qp.setPen(QColor(86, 86, 86))
            for letter in star.spectral_class:
                if letter in COLORS:
                    qp.setBrush(COLORS[letter])
            qp.drawEllipse(star.x_visual_progect - star_size / 2,
                           star.y_visual_progect - star_size / 2,
                           star_size, star_size)

    def draw_sky(self, qp):
        self.draw_layout(qp)
        self.draw_backlight(qp)
        self.draw_grid(qp)
        self.draw_progection(qp)
        self.draw_earth(qp)
        self.draw_black_frame(qp)


def main():
    app = QApplication(sys.argv)
    sky = Sky()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
