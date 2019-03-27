from wpilib.command.command import Command


class LineFollow(Command):
    _speed = None
    _finished = False

    def __init__(self, robot, speed, name=None, timeout=15):
        super().__init__(name, timeout)
        self.robot = robot
        self.requires(robot.drivetrain)
        self._speed = speed
        self._finished = False

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is schedule to run"""
        # Get line sensors state
        # NOTE: Assuming 5 sensors for this robot (can be 3)
        line_sensors = self.robot.drivetrain.get_line_follow_state()

        # Check if any sensors detect a line and drive accordingly
        # (far_left, left_line, center_line, right_line, far_right)
        if len(line_sensors) == 5:
            if line_sensors[0] == 1:
                self.robot.drivetrain.arcade_drive(0.0, -0.2, False)
            elif line_sensors[1] == 1:
                self.robot.drivetrain.arcade_drive(self._speed, -0.1, False)
            elif line_sensors[2] == 1:
                self.robot.drivetrain.arcade_drive(self._speed, 0.0, False)
            elif line_sensors[3] == 1:
                self.robot.drivetrain.arcade_drive(self._speed, 0.1, False)
            elif line_sensors[4] == 1:
                self.robot.drivetrain.arcade_drive(0.0, 0.2, False)
            else:
                self.robot.drivetrain.arcade_drive(0.0, 0.3, False)
        else:
            # No sensors available, so quit
            self._finished = True

        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return self._finished

    def end(self):
        """Called once after isFinished returns true"""
        self.robot.drivetrain.arcade_drive(0.0, 0.0, False)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
