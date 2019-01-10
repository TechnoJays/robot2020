from wpilib.command.command import Command
import math


class SetElevatorToPosition(Command):

    def __init__(self, robot, speed, encoder_position, threshold, name=None, timeout=15):
        super().__init__(name, timeout)
        self.robot = robot
        self._speed = speed
        self._encoder_target = encoder_position
        self._encoder_threshold = threshold
        self.requires(robot.elevator)

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        # Get encoder count
        current = self.robot.elevator.get_encoder_value()
        distance_left = self._encoder_target - current
        # Determine direction using target and current encoder values
        if distance_left >= 0:
            direction = 1.0
        else:
            direction = -1.0
        directional_speed = self._speed * direction
        self.robot.elevator.move_elevator(directional_speed)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        current = self.robot.elevator.get_encoder_value()
        return math.fabs(self._encoder_target - current) <= self._encoder_threshold or self.isTimedOut()

    def end(self):
        """Called once after isFinished returns true"""
        self.robot.elevator.move_elevator(0.0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
