import configparser
from enum import Enum

from wpilib._wpilib import PWMTalonSRX
from wpilib.command import Subsystem
from wpilib import I2C

from rev.color import ColorSensorV3


class ColorTarget:
    r = 0
    g = 0
    b = 0
    tolerance = 0.0

    def __init__(self, r, g, b, tolerance=0.0):
        self.r = r
        self.g = g
        self.b = b
        self.tolerance = tolerance


class ControlPanel(Subsystem):

    class Color(Enum):
        RED = "Red"
        BLUE = "Blue"
        YELLOW = "Yellow"
        GREEN = "Green"
        NONE = "None"

    GENERAL_SECTION = "ControlPanelGeneral"

    COLOR_PROFILE_KEY = "COLOR_PROFILE"
    ENABLED_KEY = "ENABLED"
    INVERTED_KEY = "INVERTED"
    CHANNEL_KEY = "CHANNEL"
    MAX_SPEED_KEY = "MAX_SPEED"

    R_KEY = "R"
    G_KEY = "G"
    B_KEY = "B"
    TOLERANCE_KEY = "TOLERANCE"

    RED_KEY = "Red"
    BLUE_KEY = "Blue"
    YELLOW_KEY = "Yellow"
    GREEN_KEY = "Green"

    _robot = None
    _color_sensor: ColorSensorV3 = None
    _motor = None

    _max_speed = 0.0

    _red_target = None
    _green_target = None
    _blue_target = None
    _yellow_target = None

    def __init__(self, robot, name=None, configfile='/home/lvuser/py/configs/subsystems.ini'):
        self._robot = robot
        self._config = configparser.ConfigParser()
        self._config.read(configfile)
        self._init_components()
        self._load_color_profile()

    def _init_components(self):
        self._max_speed = self._config.getfloat(self.GENERAL_SECTION, self.MAX_SPEED_KEY)
        if self._config.getboolean(self.GENERAL_SECTION, self.ENABLED_KEY):
            self._color_sensor = ColorSensorV3(I2C.Port.k0nboard)
            self._motor = PWMTalonSRX(self._config.getint(self.GENERAL_SECTION, self.CHANNEL_KEY))
            self._motor.setInverted(self._config.getboolean(self.GENERAL_SECTION, self.INVERTED_KEY))

    def _load_color_profile(self):
        if self._config.getboolean(self.GENERAL_SECTION, self.ENABLED_KEY):
            color_profile = self._config.get(self.GENERAL_SECTION, self.COLOR_PROFILE_KEY)
            self._red_target = self._load_color_target(color_profile, self.RED_KEY)
            self._blue_target = self._load_color_target(color_profile, self.BLUE_KEY)
            self._yellow_target = self._load_color_target(color_profile, self.YELLOW_KEY)
            self._green_target = self._load_color_target(color_profile, self.GREEN_KEY)

    def _load_color_target(self, profile, color):
        section = profile + color
        r = self._config.getint(section, self.R_KEY)
        g = self._config.getint(section, self.G_KEY)
        b = self._config.getint(section, self.B_KEY)
        tolerance = self._config.getint(section, self.TOLERANCE_KEY)
        return ColorTarget(r, g, b, tolerance)

    def get_current_color(self):
        color = self._color_sensor.getColor()
        if self._is_color_detected(color, self._red_target):
            return ControlPanel.Color.RED
        elif self._is_color_detected(color, self._blue_target):
            return ControlPanel.Color.BLUE
        elif self._is_color_detected(color, self._red_target):
            return ControlPanel.Color.YELLOW
        elif self._is_color_detected(color, self._red_target):
            return ControlPanel.Color.GREEN
        else:
            return ControlPanel.Color.NONE

    def _is_color_detected(self, target, color):
        return self._is_in_tolerance(color.r, target.r, target.tolerance) \
               and self._is_in_tolerance(color.g, target.g, target.tolerance) \
               and self._is_in_tolerance(color.b, target.b, target.tolerance)

    def move(self, speed):
        if speed < -1:
            speed = -1
        elif speed > 1:
            speed = 1
        self._motor.set(speed * self._max_speed)


    @staticmethod
    def _is_in_tolerance(value, target, tolerance):
        return (target * (1 - tolerance) < value) and (value < target * (1 + tolerance))
