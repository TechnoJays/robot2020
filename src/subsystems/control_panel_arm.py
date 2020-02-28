import configparser

from wpilib import SmartDashboard
from wpilib import Solenoid
from wpilib.command import Subsystem

from commands.do_nothing_arm import DoNothingArm


class ControlPanelArm(Subsystem):

    GENERAL_SECTION = "ControlPanelArmGeneral"

    ENABLED_KEY = "ENABLED"
    SOLENOID_CHANNEL_KEY = "SOLENOID_CHANNEL"
    SOLENOID_INVERTED_KEY = "SOLENOID_INVERTED"

    _robot = None
    _solenoid:  Solenoid = None
    _solenoid_inverted: bool = False
    _enabled: bool = False

    def __init__(self, robot, name='ControlPanelArm', configfile='/home/lvuser/py/configs/subsystems.ini'):
        self._robot = robot
        self._config = configparser.ConfigParser()
        self._config.read(configfile)
        self._enabled = self._config.getboolean(ControlPanelArm.GENERAL_SECTION, ControlPanelArm.ENABLED_KEY)
        self._init_components()
        super().__init__(name)

    def _init_components(self):
        if self._enabled:
            self._solenoid_inverted = self._config.getboolean(ControlPanelArm.GENERAL_SECTION, ControlPanelArm.SOLENOID_INVERTED_KEY)
            self._solenoid = Solenoid(self._config.getint(ControlPanelArm.GENERAL_SECTION, ControlPanelArm.SOLENOID_CHANNEL_KEY))

    def initDefaultCommand(self):
        self.setDefaultCommand(DoNothingArm(self._robot))

    def extend(self, state: bool):
        if not self._enabled:
            return
        self._solenoid.set(state ^ self._solenoid_inverted)
        ControlPanelArm.update_smartdashboard(self._solenoid.get())

    @staticmethod
    def update_smartdashboard(solenoid: bool):
        SmartDashboard.putBoolean("Control Panel Arm Solenoid", solenoid)
