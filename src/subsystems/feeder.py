from configparser import ConfigParser
from commands.feed_cube import FeedCube
from wpilib.command.subsystem import Subsystem
from wpilib.digitalinput import DigitalInput
from wpilib.talon import Talon
from wpilib.smartdashboard import SmartDashboard


class Feeder(Subsystem):
    _general_section: str = "FeederGeneral"
    _switch_section: str = "FeederSwitch"

    _enabled_key: str = "ENABLED"
    _channel_key: str = "CHANNEL"
    _inverted_key: str = "INVERTED"
    _pickup_speed_scale_key: str = "PICKUP_SPEED"
    _shoot_speed_scale_key: str = "SHOOT_SPEED"

    _motor_channel: int = None
    _switch_channel: int = None

    _motor_inverted: bool = False

    _robot = None
    _config: ConfigParser = None
    _motor: Talon = None
    _switch: DigitalInput = None

    _pickup_speed_scale: float = 0.0
    _shoot_speed_scale: float = 0.0

    def __init__(self, robot, name=None, configfile: str='/home/lvuser/py/configs/subsystems.ini'):
        super().__init__(name=name)
        self._robot = robot
        self._config = ConfigParser()
        self._config.read(configfile)
        self._init_components()
        self._update_smartdashboard()

    def initDefaultCommand(self):
        self.setDefaultCommand(FeedCube(self._robot))

    def has_cube(self) -> bool:
        if self._switch:
            return not self._switch.get()
        else:
            return False

    def feed_cube(self, speed: float):
        if self._motor:
            if speed < 0.0:
                speed = speed * self._shoot_speed_scale
                self._motor.set(speed)
            elif speed > 0.0 and not self.has_cube():
                speed = speed * self._pickup_speed_scale
                self._motor.set(speed)
            else:
                speed = 0.0
                self._motor.set(speed)
        self._update_smartdashboard()

    def _update_smartdashboard(self):
        SmartDashboard.putBoolean("Cube Acquired", self.has_cube())

    def _init_components(self):
        self._pickup_speed_scale = self._config.getfloat(self._general_section, self._pickup_speed_scale_key)
        self._shoot_speed_scale = self._config.getfloat(self._general_section, self._shoot_speed_scale_key)

        if self._config.getboolean(Feeder._general_section, Feeder._enabled_key):
            self._motor_channel = self._config.getint(self._general_section, self._channel_key)
            self._motor_inverted = self._config.getboolean(self._general_section, self._inverted_key)

        if self._motor_channel:
            self._motor = Talon(self._motor_channel)
            if self._motor_inverted:
                self._motor.setInverted(self._motor_inverted)

        if self._config.getboolean(Feeder._switch_section, Feeder._enabled_key):
            self._switch_channel = self._config.getint(self._switch_section, self._channel_key)

        if self._switch_channel:
            self._switch = DigitalInput(self._switch_channel)
