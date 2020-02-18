import wpilib
from wpilib import command

from commands.autonomous import MoveFromLine
from oi import OI
from subsystems.climbing import Climbing
from subsystems.control_panel import ControlPanel
from subsystems.drivetrain import Drivetrain


class MyRobot(wpilib.IterativeRobot):
    oi = None
    drivetrain = None
    climbing = None
    control_panel = None
    autonomous_command = None

    def autonomousInit(self):
        # Schedule the autonomous command
        self.drivetrain.reset_gyro_angle()
        self.autonomous_command = MoveFromLine(self)
        self.autonomous_command.start()

    def testInit(self):
        pass

    def teleopInit(self):
        if self.autonomous_command:
            self.autonomous_command.cancel()

    def disabledInit(self):
        pass

    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        self.oi = OI(self)
        self.drivetrain = Drivetrain(self)
        self.climbing = Climbing(self)
        self.control_panel = ControlPanel(self)
        self.oi.setup_button_bindings()
        wpilib.CameraServer.launch()

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        command.Scheduler.getInstance().run()

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        command.Scheduler.getInstance().run()

    def testPeriodic(self):
        """This function is called periodically during test mode."""
        pass


if __name__ == "__main__":
    wpilib.run(MyRobot)
