import configparser
from enum import Enum

from wpilib import PWMTalonSRX
from wpilib import Solenoid
from wpilib.command import Subsystem
from wpilib import Color
from wpilib import I2C
from wpilib import SmartDashboard

from rev.color import ColorSensorV3
from rev.color import ColorMatch

from commands.move_control_panel import MoveControlPanel


class ControlPanel(Subsystem):

    class PanelColor(Enum):
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
    _solenoid: Solenoid = None

    _max_speed: float = 0.0
    _solenoid_inverted: bool = False
    _enabled: bool = False

    _red_target: Color = None
    _green_target: Color = None
    _blue_target: Color = None
    _yellow_target: Color = None
    _color_matcher: ColorMatch = None
    _tolerance: float = None

    def __init__(self, robot, name='ControlPanel', configfile='/home/lvuser/py/configs/subsystems.ini'):
        self._robot = robot
        self._config = configparser.ConfigParser()
        self._config.read(configfile)
        self._enabled = self._config.getboolean(ControlPanel.GENERAL_SECTION, ControlPanel.ENABLED_KEY)
        self._color_matcher = ColorMatch()
        self._color_matcher.setConfidenceThreshold(self._config.getfloat(ControlPanel.GENERAL_SECTION, ControlPanel.CONFIDENCE_KEY))
        self._init_components()
        self._load_color_profile()
        super().__init__(name)

    def _init_components(self):
        self._max_speed = self._config.getfloat(ControlPanel.GENERAL_SECTION, ControlPanel.MAX_SPEED_KEY)
        self._solenoid_inverted = self._config.getboolean(ControlPanel.GENERAL_SECTION, ControlPanel.SOLENOID_INVERTED_KEY)
        if self._enabled:
            self._color_sensor = ColorSensorV3(I2C.Port.kOnboard)
            self._motor = PWMTalonSRX(self._config.getint(ControlPanel.GENERAL_SECTION, ControlPanel.MOTOR_CHANNEL_KEY))
            self._motor.setInverted(self._config.getboolean(ControlPanel.GENERAL_SECTION, ControlPanel.MOTOR_INVERTED_KEY))
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

    def _load_color_target(self, profile: str, color: str) -> Color:
        section = profile + color
        r = self._config.getfloat(section, ControlPanel.R_KEY)
        g = self._config.getfloat(section, ControlPanel.G_KEY)
        b = self._config.getfloat(section, ControlPanel.B_KEY)
        return Color(r, g, b)

    def initDefaultCommand(self):
        self.setDefaultCommand(MoveControlPanel(self, self._robot, 'MoveControlPanel'))

    def get_current_color(self) -> PanelColor:
        if not self._enabled:
            return ControlPanel.PanelColor.NONE

        color: Color = self._color_sensor.getColor()
        ControlPanel.update_smartdashboard(color)
        match_result = self._color_matcher.matchClosest(color)
        if match_result.color == self._red_target:
            return ControlPanel.PanelColor.RED
        elif match_result.color == self._blue_target:
            return ControlPanel.PanelColor.BLUE
        elif match_result.color == self._yellow_target:
            return ControlPanel.PanelColor.YELLOW
        elif match_result.color == self._green_target:
            return ControlPanel.PanelColor.GREEN
        else:
            return ControlPanel.PanelColor.NONE

    def move(self, speed: float):
        if not self._enabled:
            return
        if speed < -1:
            speed = -1
        elif speed > 1:
            speed = 1
        self._motor.set(speed * self._max_speed)

    def extend(self, state: bool):
        if not self._enabled:
            return
        self._solenoid.set(state ^ self._solenoid_inverted)

    @staticmethod
    def update_smartdashboard(color: Color):
        SmartDashboard.putFloat("Color R", color.r)
        SmartDashboard.putFloat("Color G", color.g)
        SmartDashboard.putFloat("Color B", color.b)
