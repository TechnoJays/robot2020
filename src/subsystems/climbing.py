import configparser

from wpilib import DigitalInput
from wpilib import PWMTalonSRX
from wpilib import SmartDashboard
from wpilib.command import Subsystem


class Climbing(Subsystem):
    # Config file section names
    GENERAL_SECTION = "ClimbingGeneral"
    LIMIT_SWITCH_SECTION = "ClimbingLimitSwitch"
    ENABLED_KEY = "ENABLED"
    INVERTED_KEY = "INVERTED"
    CHANNEL_KEY = "CHANNEL"
    MAX_SPEED_KEY = "MAX_SPEED"

    _max_speed = 0

    _robot = None
    _config = None
    _motor = None
    _limit_switch = None

    def __init__(self, robot, name=None, configfile='/home/lvuser/py/configs/subsystems.ini'):
        self._robot = robot
        self._config = configparser.ConfigParser()
        self._config.read(configfile)
        self._init_components()
        self._update_smartdashboard_sensors()
        super().__init__(name=name)

    def _init_components(self):
        self._max_speed = self._config.getfloat(Climbing.GENERAL_SECTION, Climbing.MAX_SPEED_KEY)
        if self._config.getboolean(Climbing.GENERAL_SECTION, Climbing.ENABLED_KEY):
            self._motor = PWMTalonSRX(self._config.getint(self.GENERAL_SECTION, Climbing.CHANNEL_KEY))
            self._motor.setInverted(self._config.getboolean(Climbing.GENERAL_SECTION, Climbing.INVERTED_KEY))
        if self._config.getboolean(Climbing.LIMIT_SWITCH_SECTION, Climbing.ENABLED_KEY):
            self._limit_switch = DigitalInput(self._config.getint(self.LIMIT_SWITCH_SECTION, Climbing.CHANNEL_KEY))

    def _update_smartdashboard_sensors(self):
        pass
        if self._limit_switch is not None:
            SmartDashboard.putBoolean("Climbing Switch", line_state[1])

        #SmartDashboard.putNumber("Drivetrain Sonar Distance", self._sonar_distance)

    def initDefaultCommand(self):
        pass
#        self.setDefaultCommand(TankDrive(self._robot, 'TankDrive', modifier_scaling=self._modifier_scaling,
#                                         dpad_scaling=self._dpad_scaling))

