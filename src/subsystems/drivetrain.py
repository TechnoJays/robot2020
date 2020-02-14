import configparser
from typing import Optional

from wpilib.command import Subsystem
from wpilib.drive import DifferentialDrive
from wpilib import PWMTalonSRX
from wpilib import ADXRS450_Gyro
from wpilib import SmartDashboard
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
    # ARCADE_DRIVE_ROTATION_INVERTED_KEY = "ARCADE_DRIVE_ROTATION_INVERTED"
    TYPE_KEY = "TYPE"
    CHANNEL_KEY = "CHANNEL"
    REVERSED_KEY = "REVERSED"
    MAX_SPEED_KEY = "MAX_SPEED"
    MODIFIER_SCALING_KEY = "MODIFIER_SCALING"
    DPAD_SCALING_KEY = "DPAD_SCALING"

    _max_speed: float = 0
    # Default arcade drive rotation modifier to -1 for DifferentialDrive
    _arcade_rotation_modifier: float = -1

    _robot = None
    _config: configparser.ConfigParser = None

    _left_motor = None
    _right_motor = None
    _robot_drive = None

    _modifier_scaling: Optional[float] = None
    _dpad_scaling: Optional[float] = None

    _sonar: Optional[MaxSonar] = None
    _sonar_distance: float = 0
    _gyro: Optional[ADXRS450_Gyro] = None
    _gyro_angle: float = 0.0

    def __init__(self, robot, name=None, configfile='/home/lvuser/py/configs/subsystems.ini'):
        self._robot = robot
        self._config = configparser.ConfigParser()
        self._config.read(configfile)
        self._init_components()
        self._update_smartdashboard_sensors(self._sonar_distance, self._gyro_angle)
        Drivetrain._update_smartdashboard_tank_drive(0.0, 0.0)
        Drivetrain._update_smartdashboard_arcade_drive(0.0, 0.0)
        super().__init__(name=name)

    def initDefaultCommand(self):
        self.setDefaultCommand(TankDrive(self._robot, 'TankDrive', modifier_scaling=self._modifier_scaling,
                                         dpad_scaling=self._dpad_scaling))

    def get_gyro_angle(self) -> float:
        if self._gyro:
            self._gyro_angle = self._gyro.getAngle()
        return self._gyro_angle

    def reset_gyro_angle(self) -> float:
        if self._gyro:
            self._gyro.reset()
            self._gyro_angle = self._gyro.getAngle()
        self._update_smartdashboard_sensors(self._sonar_distance, self._gyro_angle)
        return self._gyro_angle

    def get_sonar_distance(self) -> float:
        if self._sonar:
            self._sonar_distance = self._sonar.get_distance()
        return self._sonar_distance

    def is_gyro_enabled(self) -> bool:
        return self._gyro is not None

    def get_arcade_rotation_modifier(self) -> float:
        return self._arcade_rotation_modifier

    def tank_drive(self, left_speed: float, right_speed: float):
        left = left_speed * self._max_speed
        right = right_speed * self._max_speed
        self._robot_drive.tankDrive(left, right, False)
        Drivetrain._update_smartdashboard_tank_drive(left_speed, right_speed)
        self.get_gyro_angle()
        self.get_sonar_distance()
        self._update_smartdashboard_sensors(self._sonar_distance, self._gyro_angle)

    def arcade_drive(self, linear_distance: float, turn_angle: float, squared_inputs: bool = True):
        determined_turn_angle = self._modify_turn_angle(turn_angle)
        if self._robot_drive:
            self._robot_drive.arcadeDrive(linear_distance, determined_turn_angle, squared_inputs)
        Drivetrain._update_smartdashboard_arcade_drive(linear_distance, determined_turn_angle)
        self.get_gyro_angle()
        self.get_sonar_distance()
        self._update_smartdashboard_sensors(self._sonar_distance, self._gyro_angle)

    def _modify_turn_angle(self, turn_angle: float) -> float:
        """Method to support switch from pyfrc RobotDrive to pyfrc DifferentialDrive
        see: https://robotpy.readthedocs.io/projects/wpilib/en/latest/wpilib.drive/DifferentialDrive.html#wpilib.drive.differentialdrive.DifferentialDrive
        """
        return self._arcade_rotation_modifier * turn_angle

    @staticmethod
    def _update_smartdashboard_tank_drive(left: float, right: float):
        SmartDashboard.putNumber("Drivetrain Left Speed", left)
        SmartDashboard.putNumber("Drivetrain Right Speed", right)

    @staticmethod
    def _update_smartdashboard_arcade_drive(linear: float, turn: float):
        SmartDashboard.putNumber("Drivetrain Linear Speed", linear)
        SmartDashboard.putNumber("Drivetrain Turn Speed", turn)

    @staticmethod
    def _update_smartdashboard_sensors(sonar_distance: float, gyro_angle: float):
        SmartDashboard.putNumber("Drivetrain Sonar Distance", sonar_distance)
        SmartDashboard.putNumber("Gyro Angle", gyro_angle)

    def _init_components(self):
        self._max_speed = self._config.getfloat(Drivetrain.GENERAL_SECTION, Drivetrain.MAX_SPEED_KEY)
        self._modifier_scaling = self._config.getfloat(Drivetrain.GENERAL_SECTION, Drivetrain.MODIFIER_SCALING_KEY)
        self._dpad_scaling = self._config.getfloat(Drivetrain.GENERAL_SECTION, Drivetrain.DPAD_SCALING_KEY)

        if self._config.getboolean(Drivetrain.GYRO_SECTION, Drivetrain.ENABLED_KEY):
            self._gyro = ADXRS450_Gyro(self._config.getint(Drivetrain.GYRO_SECTION, Drivetrain.CHANNEL_KEY))

        if self._config.getboolean(Drivetrain.SONAR_SECTION, Drivetrain.ENABLED_KEY):
            self._sonar = MaxSonar(self._config.getint(Drivetrain.SONAR_SECTION, Drivetrain.CHANNEL_KEY))

        if self._config.getboolean(Drivetrain.LEFT_MOTOR_SECTION, Drivetrain.ENABLED_KEY):
            self._left_motor = PWMTalonSRX(self._config.getint(Drivetrain.LEFT_MOTOR_SECTION, Drivetrain.CHANNEL_KEY))
            self._left_motor.setInverted(self._config.getboolean(Drivetrain.LEFT_MOTOR_SECTION,
                                                                 Drivetrain.INVERTED_KEY))

        if self._config.getboolean(Drivetrain.RIGHT_MOTOR_SECTION, Drivetrain.ENABLED_KEY):
            self._right_motor = PWMTalonSRX(self._config.getint(Drivetrain.RIGHT_MOTOR_SECTION,
                                                                Drivetrain.CHANNEL_KEY))
            self._right_motor.setInverted(self._config.getboolean(Drivetrain.RIGHT_MOTOR_SECTION,
                                                                  Drivetrain.INVERTED_KEY))

        if self._left_motor and self._right_motor:
            self._robot_drive = DifferentialDrive(self._left_motor, self._right_motor)
            self._robot_drive.setSafetyEnabled(False)
