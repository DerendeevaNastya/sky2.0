import math
import sys
import stars_data
import progection
import copy
from PyQt5.QtCore import QPoint, Qt, QSize, QUrl
from PyQt5.QtGui import QPainter, QColor, QFont, QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QSlider, QMainWindow
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


COLORS = {'O': QColor(102, 253, 255),
          'B': QColor(153, 204, 255),
          'A': QColor(210, 255, 255),
          'F': QColor(255, 255, 255),
          'G': QColor(255, 247, 127),
          'K': QColor(255, 232, 79),
          'M': QColor(255, 157, 45)}

class FormParams:
    form_x = 600
    form_y = 600
    dx = 300
    dy = 0
    sky_radius = min((form_x - dx)/2 - 40, form_y / 2 - 40)
    sky_center_x = dx + sky_radius
    sky_center_y = sky_radius
    grid_flag = 0

PROGECTION = progection.Progection(FormParams)

class SkyGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setWindowTitle('Sky')
        self.setGeometry(0, 40, 600, 600)
        self.central_widget = PaintWidget()
        self.setCentralWidget(self.central_widget)
        self.create_grid_bottom()
        self.create_bright_slider()
        self.show()

    def paintEvent(self, *args, **kwargs):
        self.change_form_params()
        PROGECTION.setFormParams(FormParams)
        PROGECTION.change_visual_progection()
        return

    def create_media_player(self):
        self.player = QMediaPlayer()
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile('music/cosmic.mp3')), None)
        self.player.setVolume(30)
        self.player.play()

    def wheelEvent(self, QWheelEvent):
        point = QWheelEvent.angleDelta()
        self.change_size(point.y() / 24)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_A:
            PROGECTION.change_sky_progection_rotation(-1)
        if key == Qt.Key_D:
            PROGECTION.change_sky_progection_rotation(1)
        if key == Qt.Key_W:
            PROGECTION.change_sky_progection_head_angle(-1)
        if key == Qt.Key_S:
            PROGECTION.change_sky_progection_head_angle(1)

        if key == Qt.Key_Up:
            PROGECTION.change_sky_progectoin_location(0, 1)
        if key == Qt.Key_Down:
            PROGECTION.change_sky_progectoin_location(0, -1)
        if key == Qt.Key_Left:
            PROGECTION.change_sky_progectoin_location(1, 0)
        if key == Qt.Key_Right:
            PROGECTION.change_sky_progectoin_location(-1, 0)


    def create_bright_slider(self):
        sld = QSlider(Qt.Vertical, self)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setGeometry(100, 350, 30, 110)
        sld.valueChanged[int].connect(PROGECTION.change_sky_progection_percent_bright)
        sld.show()

    def create_grid_bottom(self):
        btn_grid = QPushButton(self)
        btn_grid.setToolTip('I/O grid')
        btn_grid.resize(70, 70)
        btn_grid.setStyleSheet("""
            QPushButton:hover { background-color: black }
            QPushButton:!hover { background-color: black }
        """)
        btn_grid.clicked.connect(self.central_widget.draw_grid)
        btn_grid.setIcon(QIcon('images/worldgrid.png'))
        btn_grid.setIconSize(QSize(70, 70))
        btn_grid.move(100, 50)
        btn_grid.show()

    def change_form_params(self):
        FormParams.form_x = self.frameSize().width()
        FormParams.form_y = self.frameSize().height()
        FormParams.sky_radius = min((FormParams.form_x - FormParams.dx)/2 - 40, FormParams.form_y / 2 - 40)
        FormParams.sky_center_x = FormParams.dx + FormParams.sky_radius
        FormParams.sky_center_y = FormParams.sky_radius
        PROGECTION.setFormParams(FormParams)


class PaintWidget(QWidget):

    def paintEvent(self, event):
        qp = QPainter(self)
        self.draw_layout(qp)
        self.draw_sky(qp)

    def draw_layout(self, qp):
        qp.setBrush(Qt.black)
        qp.drawRect(self.rect())
        qp.setPen(QColor(200, 200, 200))
        qp.drawLine(
            QPoint(FormParams.dx, 0),
            QPoint(FormParams.dx, FormParams.form_y))
        qp.setPen(QColor(86, 86, 86))
        qp.drawEllipse(FormParams.sky_center_x - FormParams.sky_radius,
                       FormParams.sky_center_y - FormParams.sky_radius,
                       FormParams.sky_radius * 2 + 2,
                       FormParams.sky_radius * 2 + 2)

    def draw_grid(self):
        FormParams.grid_flag += 1
        FormParams.grid_flag %= 2

    def draw_sky(self, qp):
        for star in PROGECTION.visual_progection:
            qp.setBrush(QColor(250, 250, 250))
            for letter in star.spectral_class:
                if letter in COLORS:
                    qp.setBrush(COLORS[letter])
            qp.drawEllipse(star.x_visual_progect, star.y_visual_progect, 4, 4)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    DEFAULT_STAR_DATA = stars_data.get_constellations()
    ex = SkyGUI()
    sys.exit(app.exec_())