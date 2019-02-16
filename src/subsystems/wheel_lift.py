import configparser
from wpilib.command.subsystem import Subsystem
from wpilib.solenoid import Solenoid
from commands.do_nothing_lift import DoNothingWheelLift


class WheelLift(Subsystem):
    """
    Note: The PCM will automatically run in closed loop mode by default whenever a
    Solenoid object is created. For most cases the Compressor object does not
    need to be instantiated or used in a robot program. This class is only required
    in cases where the robot program needs a more detailed status of the compressor or to
    enable/disable closed loop control.
    """
    # Config file section names
    LIFT_SECTION = "WheelLift"
    ENABLED_KEY = "ENABLED"
    FRONT_SOLENOID_CHANNEL_KEY = "FRONT_SOLENOID_CHANNEL"
    REAR_SOLENOID_CHANNEL_KEY = "REAR_SOLENOID_CHANNEL"

    _robot = None
    _config = None
    _front_solenoid = None
    _rear_solenoid = None

    # def __init__(self, robot, name=None, configfile='/home/lvuser/py/configs/subsystems.ini'):
    def __init__(self, robot, name=None, configfile='./configs/subsystems.ini'):
        self._robot = robot
        self._config = configparser.ConfigParser()
        self._config.read(configfile)
        self._init_components()
        super().__init__(name=name)

    def initDefaultCommand(self):
        self.setDefaultCommand(DoNothingWheelLift(self._robot))

    def set_front_solenoid(self, state):
        if self._front_solenoid:
            self._front_solenoid.set(state)

    def set_rear_solenoid(self, state):
        if self._rear_solenoid:
            self._rear_solenoid.set(state)

    # todo: add ability to enable/disable front/rear independently
    def _init_components(self):
        if self._config.getboolean(WheelLift.LIFT_SECTION, WheelLift.ENABLED_KEY):
            front_solenoid_channel = self._config.getint(WheelLift.LIFT_SECTION, WheelLift.FRONT_SOLENOID_CHANNEL_KEY)
            self._front_solenoid = Solenoid(front_solenoid_channel)
            rear_solenoid_channel = self._config.getint(WheelLift.LIFT_SECTION, WheelLift.REAR_SOLENOID_CHANNEL_KEY)
            self._rear_solenoid = Solenoid(rear_solenoid_channel)
