from configparser import ConfigParser

from wpilib.command import CommandGroup
from wpilib.command import WaitCommand

from commands.drive_time import DriveTime
from commands.raise_shooter import RaiseShooter


def use_drive_gyro(robot) -> bool:
    return robot.drivetrain.is_gyro_enabled()


class MoveFromLine(CommandGroup):
    _SECTION = "MoveFromLine"
    _DRIVE_SPEED = "DRIVE_SPEED"
    _DRIVE_TIME = "DRIVE_TIME"

    _robot = None

    _drive_speed: float = None
    _drive_time: float = None

    def __init__(self, robot, config_path: str = "/home/lvuser/py/configs/autonomous.ini"):
        """Constructor"""
        super().__init__()
        self._robot = robot
        config = ConfigParser()
        config.read(config_path)
        self._load_config(config)
        self._initialize_commands()

    def _load_config(self, parser: ConfigParser):
        self._drive_speed = parser.getfloat(self._SECTION, self._DRIVE_SPEED)
        self._drive_time = parser.getfloat(self._SECTION, self._DRIVE_TIME)

    def _initialize_commands(self):
        command = DriveTime(self._robot, self._drive_time, self._drive_speed)
        self.addSequential(command)


class DriveToWall(CommandGroup):
    _SECTION = "DriveToWall"
    _DRIVE_SPEED = "DRIVE_SPEED"
    _DRIVE_TIME = "DRIVE_TIME"

    _robot = None

    _drive_speed: float = None
    _drive_time: float = None

    def __init__(self, robot, config_path: str = "/home/lvuser/py/configs/autonomous.ini"):
        """Constructor"""
        super().__init__()
        self._robot = robot
        config = ConfigParser()
        config.read(config_path)
        self._load_config(config)
        self._initialize_commands()

    def _load_config(self, parser: ConfigParser):
        self._drive_speed = parser.getfloat(self._SECTION, self._DRIVE_SPEED)
        self._drive_time = parser.getfloat(self._SECTION, self._DRIVE_TIME)

    def _initialize_commands(self):
        command = DriveTime(self._robot, self._drive_time, self._drive_speed)
        self.addSequential(command)


class DeadReckoningScore(CommandGroup):
    _SECTION = "DeadReckoningScore"
    _DRIVE_SPEED = "DRIVE_SPEED"
    _DRIVE_TIME = "DRIVE_TIME"
    _WAIT_TIME = "WAIT_TIME"

    _robot = None

    _drive_speed: float = None
    _drive_time: float = None
    _wait_time: float = None

    def __init__(self, robot, config_path: str = "/home/lvuser/py/configs/autonomous.ini"):
        """Constructor"""
        super().__init__()
        self._robot = robot
        config = ConfigParser()
        config.read(config_path)
        self._load_config(config)
        self._initialize_commands()

    def _load_config(self, parser: ConfigParser):
        self._drive_speed = parser.getfloat(self._SECTION, self._DRIVE_SPEED)
        self._drive_time = parser.getfloat(self._SECTION, self._DRIVE_TIME)
        self._wait_time = parser.getfloat(self._SECTION, self._WAIT_TIME)

    def _initialize_commands(self):
        command = DriveTime(self._robot, self._drive_time, self._drive_speed)
        self.addSequential(command)
        command = WaitCommand(self._wait_time)
        self.addSequential(command)
        command = RaiseShooter(self._robot)
        self.addSequential(command)
