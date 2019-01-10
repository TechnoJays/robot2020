from wpilib.command.command import Command
from stopwatch import Stopwatch


class ShootLoad(Command):
    _stopwatch = None
    _start_time = None
    _duration = None
    _speed = None

    def __init__(self, robot, duration, speed: float=0.0, name=None, timeout=5):
        super().__init__(name, timeout)
        self.robot = robot
        self._stopwatch = Stopwatch()
        self._duration = duration
        self._speed = speed
        self.requires(robot.feeder)

    def initialize(self):
        """Called before the Command is run for the first time."""
        self._stopwatch.start()
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        speed = self._speed
        self.robot.feeder.feed_cube(speed)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return self._stopwatch.elapsed_time_in_secs() >= self._duration

    def end(self):
        """Called once after isFinished returns true"""
        self._stopwatch.stop()
        self.robot.feeder.feed_cube(0.0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()