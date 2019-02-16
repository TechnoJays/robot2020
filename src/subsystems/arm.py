import configparser
from wpilib.command.subsystem import Subsystem
from wpilib.talon import Talon
from wpilib.smartdashboard import SmartDashboard
from wpilib.encoder import Encoder
from commands.do_nothing_arm import DoNothingArm

class Arm(Subsystem):
    MOTOR_SECTION = "ElevatorMotor"
    ENCODER_SECTION = "ElevatorEncoder"
    SPEED_SCALING = "SPEED_SCALING"
    ENABLED = "ENABLED"
    CHANNEL = "CHANNEL"
    INVERTED = "INVERTED"
    A_CHANNEL = "A_CHANNEL"
    B_CHANNEL = "B_CHANNEL"
    REVERSED = "REVERSED"
    TYPE = "TYPE"
    TOP_BOUND = "TOP_BOUND"
    BOTTOM_BOUND = "BOTTOM_BOUND"

    _robot = None
    _subsystem_config = None
    _motor = None
    _speed_scaling = 1.0
    _encoder = None
    _encoder_value = 0
    _encoder_top_bound = None
    _encoder_bottom_bound = None

    def __init__(self, robot, name=None, configfile='/home/lvuser/py/configs/subsystems.ini'):
        self._robot = robot
        self._subsystem_config = configfile
        self._init_components()
        super().__init__(name=name)

    def initDefaultCommand(self):
        self.setDefaultCommand(DoNothingArm(self._robot))

    def move_arm(self, speed):
        if not self._motor:
            return
        scaled_speed = speed * self._speed_scaling
        self._motor.setSpeed(scaled_speed)
        self.get_encoder_value()
        self._update_smartdashboard(scaled_speed)

    def is_encoder_enabled(self):
        return self._encoder is not None

    def get_encoder_value(self):
        if self._encoder:
            self._encoder_value = self._encoder.get()
        return self._encoder_value

    def reset_encoder_value(self):
        if self._encoder:
            self._encoder.reset()
            self._encoder_value = self._encoder.get()
        return self._encoder_value

    def _update_smartdashboard(self, speed):
        SmartDashboard.putNumber("Arm Encoder", self._encoder_value)
        SmartDashboard.putNumber("Arm Speed", speed)

    def _init_components(self):

        config = configparser.ConfigParser()
        config.read(self._subsystem_config)

        if config.getboolean(self.MOTOR_SECTION, self.ENABLED):
            motor_channel = config.getint(self.MOTOR_SECTION, self.CHANNEL)
            motor_inverted = config.getboolean(self.MOTOR_SECTION, self.INVERTED)
            self._speed_scaling = config.getfloat(self.MOTOR_SECTION, self.SPEED_SCALING)
            self._motor = Talon(motor_channel)
            if self._motor:
                self._motor.setInverted(motor_inverted)

        if config.getboolean(self.ENCODER_SECTION, self.ENABLED):
            encoder_a_channel = config.getint(self.ENCODER_SECTION, self.A_CHANNEL)
            encoder_b_channel = config.getint(self.ENCODER_SECTION, self.B_CHANNEL)
            encoder_reversed = config.getboolean(self.ENCODER_SECTION, self.REVERSED)
            encoder_type = config.getint(self.ENCODER_SECTION, self.TYPE)
            self._encoder_top_bound = config.getint(self.ENCODER_SECTION, self.TOP_BOUND)
            self._encoder_bottom_bound = config.getint(self.ENCODER_SECTION, self.BOTTOM_BOUND)
            self._encoder = Encoder(encoder_a_channel, encoder_b_channel, encoder_reversed, encoder_type)
