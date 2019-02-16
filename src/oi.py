import configparser
import wpilib
from wpilib.smartdashboard import SmartDashboard
from wpilib.sendablechooser import SendableChooser
from wpilib.buttons.joystickbutton import JoystickButton
from commands.release_panel import ReleasePanel
from commands.extend_arm_to_position import ExtendArmToPosition
from commands.retract_arm_to_position import RetractArmToPosition
from commands.raise_front_wheels import RaiseFrontWheels
from commands.raise_rear_wheels import RaiseRearWheels

class JoystickAxis(object):
    """Enumerates joystick axis."""
    LEFTX = 0
    LEFTY = 1
    RIGHTX = 2
    RIGHTY = 3
    DPADX = 5
    DPADY = 6


class JoystickButtons(object):
    """Enumerates joystick buttons."""
    X = 1
    A = 2
    B = 3
    Y = 4
    LEFTBUMPER = 5
    RIGHTBUMPER = 6
    LEFTTRIGGER = 7
    RIGHTTRIGGER = 8
    BACK = 9
    START = 10


class UserController(object):
    """Enumerates the controllers."""
    DRIVER = 0
    SCORING = 1


class OI:
    """
    This class is the glue that binds the controls on the physical operator
    interface to the commands and command groups that allow control of the robot.
    """
    _config = None
    _command_config = None
    _controllers = []
    _auto_program_chooser = None
    _starting_chooser = None

    FULL_SPEED_AHEAD: float = 1.0

    # def __init__(self, robot, configfile='/home/lvuser/py/configs/joysticks.ini'):
    def __init__(self, robot, configfile='./configs/joysticks.ini'):
        self.robot = robot
        self._config = configparser.ConfigParser()
        self._config.read(configfile)
        self._init_joystick_binding()

        for i in range(2):
            self._controllers.append(self._init_joystick(i))

        self._create_smartdashboard_buttons()

    def setup_button_bindings(self):
        release_panel_button = JoystickButton(self._controllers[UserController.SCORING], JoystickButtons.A)
        release_panel_button.whileHeld(ReleasePanel(self.robot))

        raise_front_wheels_button = JoystickButton(self._controllers[UserController.DRIVER], JoystickButtons.RIGHTTRIGGER)
        raise_front_wheels_button.whileHeld(RaiseFrontWheels(self.robot))
        raise_rear_wheels_button = JoystickButton(self._controllers[UserController.DRIVER], JoystickButtons.LEFTTRIGGER)
        raise_rear_wheels_button.whileHeld(RaiseRearWheels(self.robot))

        extend_arm_button = JoystickButton(self._controllers[UserController.SCORING], JoystickButtons.X)
        # need to get an encoder position to pass into this call
        extend_arm_button.whenPressed(ExtendArmToPosition(self.robot, 1, 1))
        retract_arm_button = JoystickButton(self._controllers[UserController.SCORING], JoystickButtons.Y)
        # same deal, need encoder position
        retract_arm_button.whenPressed(RetractArmToPosition(self.robot, 1, 1))



        # open_arm_button = JoystickButton(self._controllers[UserController.SCORING], JoystickButtons.RIGHTBUMPER)
        # close_arm_button = JoystickButton(self._controllers[UserController.SCORING], JoystickButtons.RIGHTTRIGGER)
        #
        # raise_arms_button = JoystickButton(self._controllers[UserController.SCORING], JoystickButtons.Y)
        # lower_arms_button = JoystickButton(self._controllers[UserController.SCORING], JoystickButtons.A)
        #
        # raise_winch_button = JoystickButton(self._controllers[UserController.SCORING], JoystickButtons.LEFTBUMPER)
        # lower_winch_button = JoystickButton(self._controllers[UserController.SCORING], JoystickButtons.LEFTTRIGGER)

    def get_axis(self, user, axis):
        """Read axis value for specified controller/axis.

        Args:
            user: Controller ID to read from
            axis: Axis ID to read from.

        Return:
            Current position for the specified axis. (Range [-1.0, 1.0])
        """
        controller = self._controllers[user]
        value = 0.0
        if axis == JoystickAxis.DPADX:
            value = controller.getPOV()
            if value == 90:
                value = 1.0
            elif value == 270:
                value = -1.0
            else:
                value = 0.0
        elif axis == JoystickAxis.DPADY:
            value = controller.getPOV()
            if value == 0:
                value = -1.0
            elif value == 180:
                value = 1.0
            else:
                value = 0.0
        else:
            config_section = "JoyConfig" + str(user)
            dead_zone = self._config.getfloat(config_section, "DEAD_ZONE")
            value = controller.getRawAxis(axis)
            if abs(value) < dead_zone:
                value = 0.0

        return value

    def get_button_state(self, user, button):
        return self._controllers[user].getRawButton(button)

    def _create_smartdashboard_buttons(self):
        return
        # self._auto_program_chooser = SendableChooser()
        # self._auto_program_chooser.addDefault("Cross Line", 1)
        # self._auto_program_chooser.addObject("Place Cube", 2)
        # self._auto_program_chooser.addObject("Do Nothing", 3)
        # SmartDashboard.putData("Autonomous", self._auto_program_chooser)

        # self._starting_chooser = SendableChooser()
        # self._starting_chooser.addDefault("Left", 1)
        # self._starting_chooser.addObject("Center", 2)
        # self._starting_chooser.addObject("Right", 3)
        # SmartDashboard.putData("Starting_Position", self._starting_chooser)

    def get_auto_choice(self):
        return self._auto_program_chooser.getSelected()

    def get_position(self):
        value = self._starting_chooser.getSelected()
        return value

    def _init_joystick(self, driver):
        config_section = "JoyConfig" + str(driver)
        stick = wpilib.Joystick(self._config.getint(config_section, "PORT"))
        return stick

    def _init_joystick_binding(self):
        axis_binding_section = "AxisBindings"
        JoystickAxis.LEFTX = self._config.getint(axis_binding_section, "LEFTX")
        JoystickAxis.LEFTY = self._config.getint(axis_binding_section, "LEFTY")
        JoystickAxis.RIGHTX = self._config.getint(axis_binding_section, "RIGHTX")
        JoystickAxis.RIGHTY = self._config.getint(axis_binding_section, "RIGHTY")
        JoystickAxis.DPADX = self._config.getint(axis_binding_section, "DPADX")
        JoystickAxis.DPADY = self._config.getint(axis_binding_section, "DPADY")

        button_binding_section = "ButtonBindings"
        JoystickButtons.X = self._config.getint(button_binding_section, "X")
        JoystickButtons.A = self._config.getint(button_binding_section, "A")
        JoystickButtons.B = self._config.getint(button_binding_section, "B")
        JoystickButtons.Y = self._config.getint(button_binding_section, "Y")
        JoystickButtons.LEFTBUMPER = self._config.getint(button_binding_section, "LEFTBUMPER")
        JoystickButtons.RIGHTBUMPER = self._config.getint(button_binding_section, "RIGHTBUMPER")
        JoystickButtons.LEFTTRIGGER = self._config.getint(button_binding_section, "LEFTTRIGGER")
        JoystickButtons.RIGHTTRIGGER = self._config.getint(button_binding_section, "RIGHTTRIGGER")
        JoystickButtons.BACK = self._config.getint(button_binding_section, "BACK")
        JoystickButtons.START = self._config.getint(button_binding_section, "START")
