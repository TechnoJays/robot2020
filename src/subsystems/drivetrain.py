import configparser
from wpilib.command.subsystem import Subsystem
from wpilib.encoder import Encoder
from wpilib.drive import DifferentialDrive
from wpilib.spark import Spark
from wpilib.adxrs450_gyro import ADXRS450_Gyro
from wpilib.smartdashboard import SmartDashboard
from commands.tank_drive import TankDrive


class Drivetrain(Subsystem):
    # Config file section names
    GENERAL_SECTION = "DrivetrainGeneral"
    LEFT_MOTOR_SECTION = "DrivetrainLeftMotor"
    RIGHT_MOTOR_SECTION = "DrivetrainRightMotor"
    LEFT_ENCODER_SECTION = "DrivetrainLeftEncoder"
    RIGHT_ENCODER_SECTION = "DrivetrainRightEncoder"
    GYRO_SECTION = "DrivetrainGyro"
    ENABLED_KEY = "ENABLED"
    A_CHANNEL = "A_CHANNEL"
    B_CHANNEL = "B_CHANNEL"
    INVERTED_KEY = "INVERTED"
    ARCADE_DRIVE_ROTATION_INVERTED_KEY = "ARCADE_DRIVE_ROTATION_INVERTED"
    TYPE_KEY = "TYPE"
    CHANNEL_KEY = "CHANNEL"
    REVERSED_KEY = "REVERSED"
    MAX_SPEED_KEY = "MAX_SPEED"
    MODIFIER_SCALING_KEY = "MODIFIER_SCALING"
    DPAD_SCALING_KEY = "DPAD_SCALING"

    _max_speed = 0
    # Default arcade drive rotation modifier to -1 for DifferentialDrive
    _arcade_rotation_modifier = -1

    _robot = None
    _config = None

    _left_motor = None
    _right_motor = None
    _robot_drive = None

    _left_encoder = None
    _left_encoder_a_channel = None
    _left_encoder_b_channel = None
    _left_encoder_reversed = None
    _left_encoder_type = None
    _left_encoder_count = 0

    _right_encoder = None
    _right_encoder_a_channel = None
    _right_encoder_b_channel = None
    _right_encoder_reversed = None
    _right_encoder_type = None
    _right_encoder_count = 0

    _modifier_scaling = None
    _dpad_scaling = None

    _gyro = None
    _gyro_angle = 0.0

    def __init__(self, robot, name=None, configfile='/home/lvuser/py/configs/subsystems.ini'):
        self._robot = robot
        self._config = configparser.ConfigParser()
        self._config.read(configfile)
        self._init_components()
        self._update_smartdashboard_sensors()
        self._update_smartdashboard_tank_drive(0.0, 0.0)
        self._update_smartdashboard_arcade_drive(0.0, 0.0)
        super().__init__(name=name)

    def initDefaultCommand(self):
        self.setDefaultCommand(TankDrive(self._robot, 'TankDrive', modifier_scaling=self._modifier_scaling,
                                         dpad_scaling=self._dpad_scaling))

    def get_left_encoder_value(self):
        if self._left_encoder:
            self._left_encoder_count = self._left_encoder.get()
        return self._left_encoder_count

    def get_right_encoder_value(self):
        if self._right_encoder:
            self._right_encoder_count = self._right_encoder.get()
        return self._right_encoder_count

    def get_encoder_value(self):
        if self._left_encoder and self._right_encoder:
            left_value = self.get_left_encoder_value()
            right_value = self.get_right_encoder_value()
            return int(round((left_value + right_value) / 2))
        elif self._left_encoder:
            return self.get_left_encoder_value()
        elif self._right_encoder:
            return self.get_right_encoder_value()
        else:
            return 0

    def reset_left_encoder_value(self):
        if self._left_encoder:
            self._left_encoder_count = 0
        self._update_smartdashboard_sensors()
        return self._left_encoder_count

    def reset_right_encoder_value(self):
        if self._right_encoder:
            self._right_encoder_count = 0
        self._update_smartdashboard_sensors()
        return self._right_encoder_count

    def reset_encoder_value(self):
        self.reset_left_encoder_value()
        self.reset_right_encoder_value()

    def get_gyro_angle(self):
        if self._gyro:
            self._gyro_angle = self._gyro.getAngle()
        return self._gyro_angle

    def reset_gyro_angle(self):
        if self._gyro:
            self._gyro.reset()
            self._gyro_angle = self._gyro.getAngle()
        self._update_smartdashboard_sensors()
        return self._gyro_angle

    def is_encoder_enabled(self):
        return self._left_encoder is not None or self._right_encoder is not None

    def is_gyro_enabled(self):
        return self._gyro is not None

    def get_arcade_rotation_modifier(self) -> float:
        return self._arcade_rotation_modifier

    def tank_drive(self, left_speed, right_speed):
        left = left_speed * self._max_speed
        right = right_speed * self._max_speed
        self._robot_drive.tankDrive(left, right, False)
        self._update_smartdashboard_tank_drive(left_speed, right_speed)
        self.get_gyro_angle()
        self.get_left_encoder_value()
        self.get_right_encoder_value()
        self._update_smartdashboard_sensors()

    def arcade_drive(self, linear_distance, turn_angle, squared_inputs=True):
        determined_turn_angle = self._modify_turn_angle(turn_angle)
        if self._robot_drive:
            self._robot_drive.arcadeDrive(linear_distance, determined_turn_angle, squared_inputs)
        self._update_smartdashboard_arcade_drive(linear_distance, determined_turn_angle)
        self.get_gyro_angle()
        self.get_left_encoder_value()
        self.get_right_encoder_value()
        self._update_smartdashboard_sensors()

    def _modify_turn_angle(self, turn_angle: float) -> float:
        """Method to support switch from pyfrc RobotDrive to pyfrc DifferentialDrive
        see: https://robotpy.readthedocs.io/projects/wpilib/en/latest/wpilib.drive/DifferentialDrive.html#wpilib.drive.differentialdrive.DifferentialDrive
        """
        return self._arcade_rotation_modifier * turn_angle

    def _update_smartdashboard_tank_drive(self, left, right):
        SmartDashboard.putNumber("Drivetrain Left Speed", left)
        SmartDashboard.putNumber("Drivetrain Right Speed", right)

    def _update_smartdashboard_arcade_drive(self, linear, turn):
        SmartDashboard.putNumber("Drivetrain Linear Speed", linear)
        SmartDashboard.putNumber("Drivetrain Turn Speed", turn)

    def _update_smartdashboard_sensors(self):
        SmartDashboard.putNumber("Drivetrain Left Encoder", self._left_encoder_count)
        SmartDashboard.putNumber("Drivetrain Right Encoder", self._right_encoder_count)
        SmartDashboard.putNumber("Gyro Angle", self._gyro_angle)

    def _init_components(self):
        self._max_speed = self._config.getfloat(self.GENERAL_SECTION, Drivetrain.MAX_SPEED_KEY)
        self._modifier_scaling = self._config.getfloat(self.GENERAL_SECTION, Drivetrain.MODIFIER_SCALING_KEY)
        self._dpad_scaling = self._config.getfloat(self.GENERAL_SECTION, Drivetrain.DPAD_SCALING_KEY)

        if not self._config.getboolean(self.GENERAL_SECTION, "ARCADE_DRIVE_ROTATION_INVERTED"):
            self._arcade_rotation_modifier = 1

        if self._config.getboolean(Drivetrain.LEFT_ENCODER_SECTION, Drivetrain.ENABLED_KEY):
            self._left_encoder_a_channel = self._config.getint(self.LEFT_ENCODER_SECTION, Drivetrain.A_CHANNEL)
            self._left_encoder_b_channel = self._config.getint(self.LEFT_ENCODER_SECTION, Drivetrain.B_CHANNEL)
            self._left_encoder_reversed = self._config.getboolean(self.LEFT_ENCODER_SECTION, Drivetrain.REVERSED_KEY)
            self._left_encoder_type = self._config.getint(self.LEFT_ENCODER_SECTION, Drivetrain.TYPE_KEY)
            if self._left_encoder_a_channel and self._left_encoder_b_channel and self._left_encoder_type:
                self._left_encoder = Encoder(self._left_encoder_a_channel, self._left_encoder_b_channel,
                                             self._left_encoder_reversed, self._left_encoder_type)

        if self._config.getboolean(Drivetrain.RIGHT_ENCODER_SECTION, Drivetrain.ENABLED_KEY):
            self._right_encoder_a_channel = self._config.getint(self.RIGHT_ENCODER_SECTION, Drivetrain.A_CHANNEL)
            self._right_encoder_b_channel = self._config.getint(self.RIGHT_ENCODER_SECTION, Drivetrain.B_CHANNEL)
            self._right_encoder_reversed = self._config.getboolean(self.RIGHT_ENCODER_SECTION,
                                                                   Drivetrain.REVERSED_KEY)
            self._right_encoder_type = self._config.getint(self.RIGHT_ENCODER_SECTION, Drivetrain.TYPE_KEY)
            if self._right_encoder_a_channel and self._right_encoder_b_channel and self._right_encoder_type:
                self._right_encoder = Encoder(self._right_encoder_a_channel, self._right_encoder_b_channel,
                                              self._right_encoder_reversed, self._right_encoder_type)

        if self._config.getboolean(Drivetrain.GYRO_SECTION, Drivetrain.ENABLED_KEY):
            gyro_channel = self._config.getint(self.GYRO_SECTION, Drivetrain.CHANNEL_KEY)
            self._gyro = ADXRS450_Gyro(gyro_channel)

        if self._config.getboolean(Drivetrain.LEFT_MOTOR_SECTION, Drivetrain.ENABLED_KEY):
            self._left_motor = Spark(self._config.getint(self.LEFT_MOTOR_SECTION, Drivetrain.CHANNEL_KEY))
            self._left_motor.setInverted(self._config.getboolean(
                Drivetrain.LEFT_MOTOR_SECTION, Drivetrain.INVERTED_KEY))

        if self._config.getboolean(Drivetrain.RIGHT_MOTOR_SECTION, Drivetrain.ENABLED_KEY):
            self._right_motor = Spark(self._config.getint(self.RIGHT_MOTOR_SECTION, Drivetrain.CHANNEL_KEY))
            self._right_motor.setInverted(self._config.getboolean(
                Drivetrain.RIGHT_MOTOR_SECTION, Drivetrain.INVERTED_KEY))

        if self._left_motor and self._right_motor:
            self._robot_drive = DifferentialDrive(self._left_motor, self._right_motor)
            self._robot_drive.setSafetyEnabled(False)
