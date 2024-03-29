import configparser

from wpilib import PWMVictorSPX
from wpilib import SmartDashboard
from wpilib.command import Subsystem

from commands.do_nothing_vacuum import DoNothingVacuum


class Vacuum(Subsystem):
    # Config file section names
    GENERAL_SECTION = "VacuumGeneral"
    ENABLED_KEY = "ENABLED"
    INVERTED_KEY = "INVERTED"
    CHANNEL_KEY = "CHANNEL"
    MAX_SPEED_KEY = "MAX_SPEED"

    _max_speed = 0

    _robot = None
    _config = None
    _motor = None

    def __init__(self, robot, name: str = 'Vacuum', configfile='/home/lvuser/py/configs/subsystems.ini'):
        self._robot = robot
        self._config = configparser.ConfigParser()
        self._config.read(configfile)
        self._init_components()
        Vacuum._update_smartdashboard(0.0)
        super().__init__(name)

    def _init_components(self):
        self._max_speed = self._config.getfloat(Vacuum.GENERAL_SECTION, Vacuum.MAX_SPEED_KEY)
        if self._config.getboolean(Vacuum.GENERAL_SECTION, Vacuum.ENABLED_KEY):
            self._motor = PWMVictorSPX(self._config.getint(Vacuum.GENERAL_SECTION, Vacuum.CHANNEL_KEY))
            self._motor.setInverted(self._config.getboolean(Vacuum.GENERAL_SECTION, Vacuum.INVERTED_KEY))

    def initDefaultCommand(self):
        self.setDefaultCommand(DoNothingVacuum(self._robot))

    def move(self, speed: float):
        adjusted_speed = 0.0
        if self._motor:
            adjusted_speed = speed * self._max_speed
            self._motor.set(adjusted_speed)
        Vacuum._update_smartdashboard(adjusted_speed)

    @staticmethod
    def _update_smartdashboard(speed: float = 0.0):
        SmartDashboard.putNumber("Vacuum Speed", speed)
