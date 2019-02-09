from wpilib.command.command import Command

class ReleasePanel(Command):

    def __init__(self, robot, name=None, timeout=None):
        super().__init__(name, timeout)
        self.robot = robot
        self.requires(robot.panel_grabber)

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is schedule to run"""
        self.robot.panel_grabber.set_panel_release(False)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return False

    def end(self):
        """Called once after isFinished returns true"""
        self.robot.panel_grabber.set_panel_release(True)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
