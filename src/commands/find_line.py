from wpilib.command import Command
from oi import JoystickAxis, UserController
from stopwatch import Stopwatch


class FindLine(Command):
    _rotation_speed = 0.1
    _seek_time = 5000
    _stopwatch = None

    def __init__(self, robot, speed, name=None, timeout=15):
        super().__init__(name, timeout)
        self.robot = robot
        self._speed = speed
        self.requires(robot.drivetrain)
        self._stopwatch = Stopwatch()

    def initialize(self):
        """Called before the Command is run for the first time."""
        self._stopwatch.start()
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        right_stick = self.robot.oi.get_axis(UserController.SCORING, JoystickAxis.RIGHTY)
        self.robot.arm.move_arm(right_stick)
        self._stopwatch
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return False

    def end(self):
        """Called once after isFinished returns true"""
        self.robot.arm.move_arm(0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
