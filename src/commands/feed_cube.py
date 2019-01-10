from wpilib.command.command import Command
from oi import UserController, JoystickAxis

class FeedCube(Command):

    def __init__(self, robot, speed: float=0.0, name=None, timeout=5):
        super().__init__(name, timeout)
        self.robot = robot
        self._feeder_speed: float = speed
        self.requires(robot.feeder)

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        move_speed: float = self.robot.oi.get_axis(UserController.SCORING, JoystickAxis.RIGHTY)
        self.robot.feeder.feed_cube(move_speed)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        if self._feeder_speed < 0.0:
            return self.robot.feeder.has_cube()
        else:
            return False

    def end(self):
        """Called once after isFinished returns true"""
        pass

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()