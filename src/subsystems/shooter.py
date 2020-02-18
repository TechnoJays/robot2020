import configparser

from wpilib import PWMVictorSPX
from wpilib import SmartDashboard
from wpilib.command import Subsystem

from commands.do_nothing import DoNothing


class Shooter(Subsystem):
    # Config file section names
    GENERAL_SECTION = "ShooterGeneral"
    ENABLED_KEY = "ENABLED"
    INVERTED_KEY = "INVERTED"
    CHANNEL_KEY = "CHANNEL"
    MAX_SPEED_KEY = "MAX_SPEED"

    _max_speed = 0

    _robot = None
    _config = None
    _motor = None

    def __init__(self, robot, name: str ='Shooter', configfile='/home/lvuser/py/configs/subsystems.ini'):
        self._robot = robot
        self._config = configparser.ConfigParser()
        self._config.read(configfile)
        self._init_components()
        Shooter._update_smartdashboard(0.0)
        super().__init__(name)

    def _init_components(self):
        self._max_speed = self._config.getfloat(Shooter.GENERAL_SECTION, Shooter.MAX_SPEED_KEY)
        if self._config.getboolean(Shooter.GENERAL_SECTION, Shooter.ENABLED_KEY):
            self._motor = PWMVictorSPX(self._config.getint(Shooter.GENERAL_SECTION, Shooter.CHANNEL_KEY))
            self._motor.setInverted(self._config.getboolean(Shooter.GENERAL_SECTION, Shooter.INVERTED_KEY))

    def initDefaultCommand(self):
        self.setDefaultCommand(DoNothing(self._robot, 'DoNothing'))

    def move(self, speed: float):
        adjusted_speed = 0.0
        if self._motor:
            adjusted_speed = speed * self._max_speed
            self._motor.set(adjusted_speed)
        Shooter._update_smartdashboard(adjusted_speed)

    @staticmethod
    def _update_smartdashboard(speed: float = 0.0):
        SmartDashboard.putNumber("Shooter Speed", speed)
