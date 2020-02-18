import configparser
from enum import Enum

from wpilib import PWMTalonSRX
from wpilib import Solenoid
from wpilib.command import Subsystem
from wpilib import I2C

from rev.color import ColorSensorV3
from rev.color import CIEColor
from rev.color import ColorMatch


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
    MOTOR_INVERTED_KEY = "MOTOR_INVERTED"
    MOTOR_CHANNEL_KEY = "MOTOR_CHANNEL"
    MAX_SPEED_KEY = "MAX_SPEED"
    SOLENOID_CHANNEL_KEY = "SOLENOID_CHANNEL"
    SOLENOID_INVERTED_KEY = "SOLENOID_INVERTED"
    CONFIDENCE_KEY = "CONFIDENCE"

    R_KEY = "R"
    G_KEY = "G"
    B_KEY = "B"

    RED_KEY = "Red"
    BLUE_KEY = "Blue"
    YELLOW_KEY = "Yellow"
    GREEN_KEY = "Green"

    _robot = None
    _color_sensor: ColorSensorV3 = None
    _motor = None
    _extender = None
    _solenoid = None

    _max_speed = 0.0
    _solenoid_inverted = False
    _enabled = False

    _red_target: CIEColor = None
    _green_target: CIEColor = None
    _blue_target: CIEColor = None
    _yellow_target: CIEColor = None
    _color_matcher: ColorMatch = None
    _tolerance: float = None

    def __init__(self, robot, name=None, configfile='/home/lvuser/py/configs/subsystems.ini'):
        self._robot = robot
        self._config = configparser.ConfigParser()
        self._config.read(configfile)
        self._enabled = self._config.getboolean(self.GENERAL_SECTION, self.ENABLED_KEY)
        self._color_matcher = ColorMatch()
        self._color_matcher.setConfidenceThreshold(self._config.getfloat(ControlPanel.GENERAL_SECTION, ControlPanel.CONFIDENCE_KEY))
        self._init_components()
        self._load_color_profile()

    def _init_components(self):
        self._max_speed = self._config.getfloat(ControlPanel.GENERAL_SECTION, ControlPanel.MAX_SPEED_KEY)
        self._solenoid_inverted = self._config.getboolean(ControlPanel.GENERAL_SECTION, ControlPanel.SOLENOID_INVERTED_KEY)
        if self._enabled:
            self._color_sensor = ColorSensorV3(I2C.Port.k0nboard)
            self._motor = PWMTalonSRX(self._config.getint(ControlPanel.GENERAL_SECTION, ControlPanel.CHANNEL_KEY))
            self._motor.setInverted(self._config.getboolean(ControlPanel.GENERAL_SECTION, ControlPanel.INVERTED_KEY))
            self._solenoid = Solenoid(self._config.getint(ControlPanel.GENERAL_SECTION, ControlPanel.SOLENOID_CHANNEL_KEY))

    def _load_color_profile(self):
        if self._enabled:
            color_profile = self._config.get(ControlPanel.GENERAL_SECTION, ControlPanel.COLOR_PROFILE_KEY)
            self._red_target = self._load_color_target(color_profile, ControlPanel.RED_KEY)
            self._color_matcher.addColorMatch(self._red_target)
            self._blue_target = self._load_color_target(color_profile, ControlPanel.BLUE_KEY)
            self._color_matcher.addColorMatch(self._blue_target)
            self._yellow_target = self._load_color_target(color_profile, ControlPanel.YELLOW_KEY)
            self._color_matcher.addColorMatch(self._yellow_target)
            self._green_target = self._load_color_target(color_profile, ControlPanel.GREEN_KEY)
            self._color_matcher.addColorMatch(self._green_target)

    def _load_color_target(self, profile: str, color: str) -> CIEColor:
        section = profile + color
        r = self._config.getfloat(section, ControlPanel.R_KEY)
        g = self._config.getfloat(section, ControlPanel.G_KEY)
        b = self._config.getfloat(section, ControlPanel.B_KEY)
        return ColorMatch.makeColor(r, g, b)

    def get_current_color(self):
        if not self._enabled:
            return ControlPanel.Color.NONE

        color = self._color_sensor.getColor()
        match_result = self._color_matcher.matchClosest(color)
        if match_result.color == self._red_target:
            return ControlPanel.Color.RED
        elif match_result.color == self._red_target:
            return ControlPanel.Color.BLUE
        elif match_result.color == self._red_target:
            return ControlPanel.Color.YELLOW
        elif match_result.color == self._red_target:
            return ControlPanel.Color.GREEN
        else:
            return ControlPanel.Color.NONE

    def move(self, speed: float):
        if not self._enabled:
            return
        
        if speed < -1:
            speed = -1
        elif speed > 1:
            speed = 1
        self._motor.set(speed * self._max_speed)

    def extend(self, state: bool):
        self._solenoid.set(state ^ self._solenoid_inverted)

