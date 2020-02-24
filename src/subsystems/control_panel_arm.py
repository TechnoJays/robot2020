import configparser

from wpilib import Solenoid
from wpilib.command import Subsystem

from commands.lower_arm import LowerArm
from commands.raise_arm import RaiseArm

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
        self._load_color_profile()
        super().__init__(name)

    def _init_components(self):
        self._solenoid_inverted = self._config.getboolean(ControlPanelArm.GENERAL_SECTION, ControlPanelArm.SOLENOID_INVERTED_KEY)
        if self._enabled:
            self._motor.setInverted(self._config.getboolean(ControlPanelArm.GENERAL_SECTION, ControlPanelArm.MOTOR_INVERTED_KEY))
            self._solenoid = Solenoid(self._config.getint(ControlPanelArm.GENERAL_SECTION, ControlPanelArm.SOLENOID_CHANNEL_KEY))

    def initDefaultCommand(self):
        self.setDefaultCommand(LowerArm(self._robot))

    def extend(self, state: bool):
        if not self._enabled:
            return
        self._solenoid.set(state ^ self._solenoid_inverted)

    @staticmethod
    def update_smartdashboard(self):
        SmartDashboard.putBoolean("Control Panel Arm Solenoid", self._solenoid.get())