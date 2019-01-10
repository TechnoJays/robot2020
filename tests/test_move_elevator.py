import pytest
import oi
from subsystems.elevator import Elevator
from commands.move_elevator import MoveElevator


@pytest.fixture(scope="function")
def elevator_default(robot):
    return Elevator(robot, None, '../tests/test_configs/elevator_default.ini')


@pytest.fixture(scope="function")
def mock_oi(robot):
    class OI:
        driver_axis_values = {oi.JoystickAxis.LEFTX: 0.0, oi.JoystickAxis.LEFTY: 0.0,
                              oi.JoystickAxis.RIGHTX: 0.0, oi.JoystickAxis.RIGHTY: 0.0,
                              oi.JoystickAxis.DPADX: 0.0, oi.JoystickAxis.DPADY: 0.0}
        scoring_axis_values = {oi.JoystickAxis.LEFTX: 0.0, oi.JoystickAxis.LEFTY: 0.0,
                               oi.JoystickAxis.RIGHTX: 0.0, oi.JoystickAxis.RIGHTY: 0.0,
                               oi.JoystickAxis.DPADX: 0.0, oi.JoystickAxis.DPADY: 0.0}
        axis_values = {oi.UserController.DRIVER: driver_axis_values,
                       oi.UserController.SCORING: scoring_axis_values}

        driver_button_values = {oi.JoystickButtons.A: False, oi.JoystickButtons.B: False,
                                oi.JoystickButtons.X: False, oi.JoystickButtons.Y: False,
                                oi.JoystickButtons.BACK: False, oi.JoystickButtons.START: False,
                                oi.JoystickButtons.LEFTBUMPER: False, oi.JoystickButtons.RIGHTBUMPER: False,
                                oi.JoystickButtons.LEFTTRIGGER: False, oi.JoystickButtons.RIGHTTRIGGER: False}
        scoring_button_values = {oi.JoystickButtons.A: False, oi.JoystickButtons.B: False,
                                 oi.JoystickButtons.X: False, oi.JoystickButtons.Y: False,
                                 oi.JoystickButtons.BACK: False, oi.JoystickButtons.START: False,
                                 oi.JoystickButtons.LEFTBUMPER: False, oi.JoystickButtons.RIGHTBUMPER: False,
                                 oi.JoystickButtons.LEFTTRIGGER: False, oi.JoystickButtons.RIGHTTRIGGER: False}
        button_values = {oi.UserController.DRIVER: driver_button_values,
                         oi.UserController.SCORING: scoring_button_values}

        def set_mock_axis_value(self, controller, axis, value):
            self.axis_values[controller][axis] = value

        def get_axis(self, controller, axis):
            return self.axis_values[controller][axis]

        def set_mock_button_value(self, controller, button, value):
            self.button_values[controller][button] = value

        def get_button_state(self, user, button):
            return self.button_values[user][button]

    return OI()


@pytest.fixture(scope="function")
def command_default(robot, elevator_default):
    robot.elevator = elevator_default
    return MoveElevator(robot, None, 15)


def test_init_default(command_default):
    assert command_default is not None
    assert command_default.robot is not None
    assert command_default.robot.elevator is not None
    assert command_default.name == "MoveElevator"
    assert command_default.timeout == 15


def test_init_full(robot, elevator_default):
    robot.elevator = elevator_default
    me = MoveElevator(robot, "CustomElevator", 5)
    assert me is not None
    assert me.robot is not None
    assert me.robot.elevator is not None
    assert me.name == "CustomElevator"
    assert me.timeout == 5


def test_initialize(command_default):
    pass  # initialize method is empty


@pytest.mark.parametrize(
    "user_input,ex_speed", [
        (0.0, 0.0),
        (0.5, 0.5),
        (1.0, 1.0),
        (-0.5, -0.5),
        (-1.0, -1.0),
    ])
def test_execute(robot, mock_oi, hal_data, elevator_default, user_input, ex_speed):
    robot.elevator = elevator_default
    robot.oi = mock_oi
    me = MoveElevator(robot, None, None)
    assert me is not None
    me.initialize()
    mock_oi.set_mock_axis_value(oi.UserController.SCORING, oi.JoystickAxis.LEFTY, user_input)
    me.execute()
    assert hal_data['pwm'][3]['value'] == ex_speed


def test_is_finished(command_default):
    assert command_default.isFinished() is False


def test_interrupted(command_default):
    pass  # interrupted method is empty


def test_end(robot, command_default):
    pass  # end method is empty
