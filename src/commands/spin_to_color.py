from wpilib.command import Command

from subsystems.control_panel import ControlPanel


class SpinToColor(Command):
    _target_color: ControlPanel.PanelColor = ControlPanel.PanelColor.NONE
    _speed: float = 1.0

    # This year the game message is a single character denoting the color target. It is "" until stage 3
    _color_target_map = {
        "": ControlPanel.PanelColor.NONE,
        "R": ControlPanel.PanelColor.RED,
        "G": ControlPanel.PanelColor.GREEN,
        "B": ControlPanel.PanelColor.BLUE,
        "Y": ControlPanel.PanelColor.YELLOW,
    }

    def __init__(self, robot, speed: float, name='SpinToColor', timeout=16):
        """Constructor"""
        super().__init__(name, timeout)
        self.robot = robot
        self.requires(robot.control_panel)
        self._speed = speed

    def initialize(self):
        """Called before the Command is run for the first time."""
        # Get the target color from the game message via FMS
        target_color_char = self.robot.oi.get_game_message()
        if target_color_char in self._color_target_map:
            self._target_color = self._color_target_map.get(target_color_char)
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self.robot.control_panel.move(self._speed)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        current_color = self.robot.control_panel.get_current_color()
        return (self._target_color == ControlPanel.PanelColor.NONE) or \
               (self.robot.control_panel.get_scored_color(current_color) == self._target_color) or self.isTimedOut()

    def end(self):
        """Called once after isFinished returns true"""
        self.robot.control_panel.move(0.0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
