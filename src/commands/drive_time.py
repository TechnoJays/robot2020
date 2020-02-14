from wpilib.command import Command
from util.stopwatch import Stopwatch


class DriveTime(Command):
    _stopwatch: Stopwatch = None
    _duration: float = None
    _speed: float = None

    def __init__(self, robot, duration: float, speed: float, name=None, timeout=15):
        """Constructor"""
        super().__init__(name, timeout)
        self.robot = robot
        self.requires(robot.drivetrain)
        self._stopwatch = Stopwatch()
        self._duration = duration
        self._speed = speed

    def initialize(self):
        """Called before the Command is run for the first time."""
        self._stopwatch.start()
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self.robot.drivetrain.arcade_drive(self._speed, 0.0, False)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return self._stopwatch.elapsed_time_in_secs() >= self._duration

    def end(self):
        """Called once after isFinished returns true"""
        self._stopwatch.stop()
        self.robot.drivetrain.arcade_drive(0.0, 0.0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
