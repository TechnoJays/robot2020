import configparser
from wpilib.command.subsystem import Subsystem
from wpilib.pwmtalonsrx import PWMTalonSRX
from wpilib.smartdashboard import SmartDashboard
from wpilib.analogpotentiometer import AnalogPotentiometer
from commands.move_arm import MoveArm


class Arm(Subsystem):
    MOTOR_SECTION = "ArmMotor"
    POTENTIOMETER_SECTION = "ArmPotentiometer"
    SPEED_SCALING = "SPEED_SCALING"
    ENABLED = "ENABLED"
    CHANNEL = "CHANNEL"
    INVERTED = "INVERTED"
    TOP_BOUND = "TOP_BOUND"
    BOTTOM_BOUND = "BOTTOM_BOUND"
    SCALING = "SCALING"
    OFFSET = "OFFSET"

    _robot = None
    _subsystem_config = None
    _motor = None
    _speed_scaling = 0.2
    _potentiometer = None
    _potentiometer_value = 0.0
    _top_bound = None
    _bottom_bound = None

    def __init__(self, robot, name=None, configfile='/home/lvuser/py/configs/subsystems.ini'):
        self._robot = robot
        self._subsystem_config = configfile
        self._init_components()
        super().__init__(name=name)

    def initDefaultCommand(self):
        self.setDefaultCommand(MoveArm(self._robot, 1.0))

    def move_arm(self, speed):
        if not self._motor:
            return
        scaled_speed = speed * self._speed_scaling
        # Get current pot value and compare against bounds
        self.get_potentiometer_value()
        if self.is_potentiometer_enabled and ((scaled_speed < 0.0 and self._potentiometer_value >= self._top_bound) or
                                              (scaled_speed > 0.0 and self._potentiometer_value <= self._bottom_bound)):
            return
        self._motor.setSpeed(scaled_speed)
        self._update_smartdashboard(scaled_speed)

    def is_potentiometer_enabled(self):
        return self._potentiometer is not None

    def get_potentiometer_value(self):
        if self._potentiometer:
            self._potentiometer_value = self._potentiometer.get()
        return self._potentiometer_value

    def _update_smartdashboard(self, speed):
        SmartDashboard.putNumber("Arm Pot", self._potentiometer_value)
        SmartDashboard.putNumber("Arm Speed", speed)

    def _init_components(self):

        config = configparser.ConfigParser()
        config.read(self._subsystem_config)

        if config.getboolean(self.MOTOR_SECTION, self.ENABLED):
            motor_channel = config.getint(self.MOTOR_SECTION, self.CHANNEL)
            motor_inverted = config.getboolean(self.MOTOR_SECTION, self.INVERTED)
            self._speed_scaling = config.getfloat(self.MOTOR_SECTION, self.SPEED_SCALING)
            self._motor = PWMTalonSRX(motor_channel)
            if self._motor:
                self._motor.setInverted(motor_inverted)

        if config.getboolean(self.POTENTIOMETER_SECTION, self.ENABLED):
            channel = config.getint(self.POTENTIOMETER_SECTION, self.CHANNEL)
            scaling = config.getfloat(self.POTENTIOMETER_SECTION, self.SCALING)
            offset = config.getfloat(self.POTENTIOMETER_SECTION, self.OFFSET)
            self._top_bound = config.getint(self.POTENTIOMETER_SECTION, self.TOP_BOUND)
            self._bottom_bound = config.getint(self.POTENTIOMETER_SECTION, self.BOTTOM_BOUND)
            self._potentiometer = AnalogPotentiometer(channel, scaling, offset)
