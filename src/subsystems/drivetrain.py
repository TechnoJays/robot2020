import configparser

from wpilib import DigitalInput
from wpilib.command.subsystem import Subsystem
from wpilib.drive import DifferentialDrive
from wpilib.pwmtalonsrx import PWMTalonSRX
from wpilib.adxrs450_gyro import ADXRS450_Gyro
from wpilib.smartdashboard import SmartDashboard
from util.sonar import MaxSonar
from commands.tank_drive import TankDrive

class Drivetrain(Subsystem):
    # Config file section names
    GENERAL_SECTION = "DrivetrainGeneral"
    LEFT_MOTOR_SECTION = "DrivetrainLeftMotor"
    RIGHT_MOTOR_SECTION = "DrivetrainRightMotor"
    GYRO_SECTION = "DrivetrainGyro"
    SONAR_SECTION = "DrivetrainSonar"
    ENABLED_KEY = "ENABLED"
    INVERTED_KEY = "INVERTED"
    LINEFOLLOW_SECTION = "DrivetrainLineFollow"
    COUNT_KEY = "COUNT"
    FAR_LEFT_KEY = "FAR_LEFT_CHANNEL"
    LEFT_KEY = "LEFT_CHANNEL"
    CENTER_KEY = "CENTER_CHANNEL"
    RIGHT_KEY = "RIGHT_CHANNEL"
    FAR_RIGHT_KEY = "FAR_RIGHT_CHANNEL"

    # ARCADE_DRIVE_ROTATION_INVERTED_KEY = "ARCADE_DRIVE_ROTATION_INVERTED"
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

    _far_left_line_follow = None
    _left_line_follow = None
    _center_line_follow = None
    _right_line_follow = None
    _far_right_line_follow = None

    _sonar: MaxSonar = None
    _sonar_distance: float = 0

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

    def get_line_follow_state(self):
        if self._far_left_line_follow and self._far_right_line_follow:
            return (self._far_left_line_follow.get(),
                    self._left_line_follow.get(),
                    self._center_line_follow.get(),
                    self._right_line_follow.get(),
                    self._far_right_line_follow.get())
        elif self._left_line_follow and self._center_line_follow and self._right_line_follow:
            return (self._left_line_follow.get(),
                    self._center_line_follow.get(),
                    self._right_line_follow.get())
        else:
            return ()

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

    def get_sonar_distance(self) -> float:
        if self._sonar:
            self._sonar_distance = self._sonar.getDistance()
        return self._sonar_distance

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
        self.get_sonar_distance()
        self._update_smartdashboard_sensors()

    def arcade_drive(self, linear_distance, turn_angle, squared_inputs=True):
        determined_turn_angle = self._modify_turn_angle(turn_angle)
        if self._robot_drive:
            self._robot_drive.arcadeDrive(linear_distance, determined_turn_angle, squared_inputs)
        self._update_smartdashboard_arcade_drive(linear_distance, determined_turn_angle)
        self.get_gyro_angle()
        self.get_sonar_distance()
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
        SmartDashboard.putNumber("Drivetrain Sonar Distance", self._sonar_distance)
        SmartDashboard.putNumber("Gyro Angle", self._gyro_angle)
        line_state = self.get_line_follow_state()
        if len(line_state) > 3:
            SmartDashboard.putBoolean("Far Left Line", line_state[0])
            SmartDashboard.putBoolean("Far Right Line", line_state[4])
        SmartDashboard.putBoolean("Left Line", line_state[1])
        SmartDashboard.putBoolean("Right Line", line_state[3])
        SmartDashboard.putBoolean("Center Line", line_state[2])

    def _init_components(self):
        self._max_speed = self._config.getfloat(self.GENERAL_SECTION, Drivetrain.MAX_SPEED_KEY)
        self._modifier_scaling = self._config.getfloat(self.GENERAL_SECTION, Drivetrain.MODIFIER_SCALING_KEY)
        self._dpad_scaling = self._config.getfloat(self.GENERAL_SECTION, Drivetrain.DPAD_SCALING_KEY)

        if self._config.getboolean(Drivetrain.GYRO_SECTION, Drivetrain.ENABLED_KEY):
            gyro_channel = self._config.getint(self.GYRO_SECTION, Drivetrain.CHANNEL_KEY)
            self._gyro = ADXRS450_Gyro(gyro_channel)

        if self._config.getboolean(Drivetrain.SONAR_SECTION, Drivetrain.ENABLED_KEY):
            sonar_channel = self._config.getint(self.SONAR_SECTION, Drivetrain.CHANNEL_KEY)
            self._sonar = MaxSonar(sonar_channel)

        if self._config.getboolean(Drivetrain.LEFT_MOTOR_SECTION, Drivetrain.ENABLED_KEY):
            self._left_motor = PWMTalonSRX(self._config.getint(self.LEFT_MOTOR_SECTION, Drivetrain.CHANNEL_KEY))
            self._left_motor.setInverted(self._config.getboolean(
                Drivetrain.LEFT_MOTOR_SECTION, Drivetrain.INVERTED_KEY))

        if self._config.getboolean(Drivetrain.RIGHT_MOTOR_SECTION, Drivetrain.ENABLED_KEY):
            self._right_motor = PWMTalonSRX(self._config.getint(self.RIGHT_MOTOR_SECTION, Drivetrain.CHANNEL_KEY))
            self._right_motor.setInverted(self._config.getboolean(
                Drivetrain.RIGHT_MOTOR_SECTION, Drivetrain.INVERTED_KEY))

        if self._config.getboolean(Drivetrain.LINEFOLLOW_SECTION, Drivetrain.ENABLED_KEY):
            sensor_count = self._config.getint(Drivetrain.LINEFOLLOW_SECTION, Drivetrain.COUNT_KEY)
            if sensor_count > 3:
                far_left_line_channel = self._config.getint(Drivetrain.LINEFOLLOW_SECTION, Drivetrain.FAR_LEFT_KEY)
                far_right_line_channel = self._config.getint(Drivetrain.LINEFOLLOW_SECTION, Drivetrain.FAR_RIGHT_KEY)
                if far_left_line_channel and far_right_line_channel:
                    self._far_left_line_follow = DigitalInput(far_left_line_channel)
                    self._far_right_line_follow = DigitalInput(far_right_line_channel)

            left_line_follow_channel = self._config.getint(Drivetrain.LINEFOLLOW_SECTION, Drivetrain.LEFT_KEY)
            right_line_follow_channel = self._config.getint(Drivetrain.LINEFOLLOW_SECTION, Drivetrain.RIGHT_KEY)
            if left_line_follow_channel and right_line_follow_channel:
                self._left_line_follow = DigitalInput(left_line_follow_channel)
                self._right_line_follow = DigitalInput(right_line_follow_channel)

            center_line_follow_channel = self._config.getint(Drivetrain.LINEFOLLOW_SECTION, Drivetrain.CENTER_KEY)
            if center_line_follow_channel:
                self._center_line_follow = DigitalInput(center_line_follow_channel)

        if self._left_motor and self._right_motor:
            self._robot_drive = DifferentialDrive(self._left_motor, self._right_motor)
            self._robot_drive.setSafetyEnabled(False)
