from wpilib.command.command import Command

class MoveArmLaterally(Command):

    def __init__(self, robot, speed: float=0.0, name=None, timeout=5):
        super().__init__(name, timeout)
        self.robot = robot
        self._arm_speed: float = speed * -1.0
        self.requires(robot.arm)

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self.robot.arm.move_arm_laterally(self._arm_speed)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return False

    def end(self):
        """Called once after isFinished returns true"""
        self.robot.arm.move_arm_laterally(0.0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()