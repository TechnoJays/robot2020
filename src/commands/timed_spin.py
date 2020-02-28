from wpilib.command import Command
from util.stopwatch import Stopwatch


class TimedSpin(Command):
    _stopwatch: Stopwatch = None
    _duration: float = None
    _speed: float = None

    def __init__(self, robot, duration: float, speed: float, name='TimedSpin', timeout=32):
        """Constructor"""
        super().__init__(name, timeout)
        self.robot = robot
        self.requires(robot.control_panel)
        self._stopwatch = Stopwatch()
        self._duration = duration
        self._speed = speed

    def initialize(self):
        """Called before the Command is run for the first time."""
        self._stopwatch.start()
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self.robot.control_panel.move(self._speed)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return self._stopwatch.elapsed_time_in_secs() >= self._duration or self.isTimedOut()

    def end(self):
        """Called once after isFinished returns true"""
        self._stopwatch.stop()
        self.robot.control_panel.move(0.0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
