import configparser
from wpilib.command.subsystem import Subsystem
from wpilib.solenoid import Solenoid
from commands.do_nothing_grabber import DoNothingPanelGrabber

class PanelGrabber(Subsystem):
    """
        Note: The PCM will automatically run in closed loop mode by default whenever a
        Solenoid object is created. For most cases the Compressor object does not
        need to be instantiated or used in a robot program. This class is only required
        in cases where the robot program needs a more detailed status of the compressor or to
        enable/disable closed loop control.
        """
    # Config file section names
    PANEL_SECTION = "PanelGrabber"
    ENABLED_KEY = "ENABLED"
    SOLENOID_CHANNEL_KEY = "SOLENOID_CHANNEL"

    _robot = None
    _config = None
    _solenoid = None

    # def __init__(self, robot, name=None, configfile='/home/lvuser/py/configs/subsystems.ini'):
    def __init__(self, robot, name=None, configfile='./configs/subsystems.ini'):
        self._robot = robot
        self._config = configparser.ConfigParser()
        self._config.read(configfile)
        self._init_components()
        super().__init__(name=name)

    def initDefaultCommand(self):
        self.setDefaultCommand(DoNothingPanelGrabber(self._robot))

    def set_panel_release(self, state):
        if self._solenoid:
            self._solenoid.set(state)

    def _init_components(self):
        if self._config.getboolean(PanelGrabber.PANEL_SECTION, PanelGrabber.ENABLED_KEY):
            solenoid_channel = self._config.getint(PanelGrabber.PANEL_SECTION, PanelGrabber.SOLENOID_CHANNEL_KEY)
            self._solenoid = Solenoid(solenoid_channel)
