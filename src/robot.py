import wpilib
from wpilib import command


from commands.do_nothing import DoNothing
from oi import OI
from subsystems.drivetrain import Drivetrain
from subsystems.panel_grabber import PanelGrabber
from subsystems.arm import Arm
from subsystems.wheel_lift import WheelLift


class MyRobot(wpilib.IterativeRobot):
    oi = None
    drivetrain = None
    arm = None
    wheel_lift = None
    panel_grabber = None
    autonomous_command = None

    def autonomousInit(self):
        # Schedule the autonomous command
        self.drivetrain.reset_gyro_angle()
        self.autonomous_command = DoNothing(self)
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
        self.arm = Arm(self)
        self.wheel_lift = WheelLift(self)
        self.panel_grabber = PanelGrabber(self)
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
