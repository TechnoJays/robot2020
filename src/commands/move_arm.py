from wpilib.command.command import Command
from oi import JoystickAxis, UserController

class MoveArm(Command):

     def __init__(self, robot, speed, name=None, timeout=15):
        super().__init__(name, timeout)
        self.robot = robot
        self._speed = speed
        self.requires(robot.arm)

     def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

     def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        right_stick = self.robot.oi.get_axis(UserController.SCORING, JoystickAxis.RIGHTY)
        if right_stick > 0.0:
            self.robot.arm.move_arm(right_stick)
        else:
            self.robot.arm.move_arm(0.0)
        return Command.execute(self)

     def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return False

     def end(self):
        """Called once after isFinished returns true"""
        pass

     def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
