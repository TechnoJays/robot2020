from wpilib.command.command import Command
from stopwatch import Stopwatch


class MoveElevatorTime(Command):

    def __init__(self, robot, directional_speed, duration, name=None, timeout=15):
        super().__init__(name, timeout)
        self.robot = robot
        self._speed = directional_speed
        self._duration = duration
        self._stopwatch = Stopwatch()
        self.requires(robot.elevator)

    def initialize(self):
        """Called before the Command is run for the first time."""
        self._stopwatch.start()
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self.robot.elevator.move_elevator(self._speed)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return self._stopwatch.elapsed_time_in_secs() >= self._duration

    def end(self):
        """Called once after isFinished returns true"""
        self._stopwatch.stop()
        self.robot.elevator.move_elevator(0.0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
