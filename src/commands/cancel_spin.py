from wpilib.command import Command


class CancelSpin(Command):
    def __init__(self, robot, name="CancelSpin", timeout=1.0):
        """Constructor"""
        super().__init__(name, timeout)
        self.robot = robot
        self.requires(robot.control_panel)

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self.robot.control_panel.move(0.0)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return self.isTimedOut()

    def end(self):
        """Called once after isFinished returns true"""
        self.robot.control_panel.move(0.0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
