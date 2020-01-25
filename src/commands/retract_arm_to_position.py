from wpilib.command import Command


class RetractArmToPosition(Command):

    def __init__(self, robot, speed, encoder_position, name=None, timeout=15):
        super().__init__(name, timeout)
        self.robot = robot
        self._speed = speed
        self._encoder_target = encoder_position
        self.requires(robot.arm)

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self.robot.arm.move_arm(self._speed * -1.0)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return self.robot.arm.get_encoder_value() >= self._encoder_target or self.isTimedOut()

    def end(self):
        """Called once after isFinished returns true"""
        self.robot.arm.move_arm(0.0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
