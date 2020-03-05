from wpilib.command import Command


class Vacuum(Command):
    _speed: float = None

    def __init__(self, robot, speed: float, name='Vacuum', timeout=15):
        super().__init__(name, timeout)
        self.robot = robot
        self._speed = speed
        self.requires(robot.vacuum)

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self.robot.vacuum.move(self._speed)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return False

    def end(self):
        """Called once after isFinished returns true"""
        self.robot.vacuum.move(0.0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
