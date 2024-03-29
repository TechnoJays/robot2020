from wpilib.command import Command
from oi import UserController, JoystickAxis


class MoveWinch(Command):
    def __init__(self, robot, name=None, timeout=15):
        """Constructor"""
        super().__init__(name, timeout)
        self.robot = robot
        self.requires(robot.climbing)

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        move_speed = self.robot.oi.get_axis(UserController.SCORING, JoystickAxis.LEFTY)
        self.robot.climbing.move_winch(move_speed)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return False

    def end(self):
        """Called once after isFinished returns true"""
        self.robot.climbing.move_winch(0.0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
