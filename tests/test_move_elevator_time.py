import pytest
from subsystems.elevator import Elevator
from commands.move_elevator_time import MoveElevatorTime
from stopwatch import Stopwatch


@pytest.fixture(scope="function")
def elevator_default(robot):
    return Elevator(robot, None, '../tests/test_configs/elevator_default.ini')


def isclose(a, b, rel_tol=0.1, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def test_init_default(robot, elevator_default):
    robot.elevator = elevator_default
    met = MoveElevatorTime(robot, 1.0, 2.0)
    assert met is not None
    assert met.robot is not None
    assert met.robot.elevator is not None
    assert met.name == "MoveElevatorTime"
    assert met.timeout == 15


def test_init_full(robot, elevator_default):
    robot.elevator = elevator_default
    met = MoveElevatorTime(robot, 1.0, 2.0, "CustomElevator", 5)
    assert met is not None
    assert met.robot is not None
    assert met.robot.elevator is not None
    assert met.name == "CustomElevator"
    assert met.timeout == 5


@pytest.mark.parametrize("speed,ex_speed", [
    (0.0, 0.0),
    (0.5, 0.5),
    (1.0, 1.0),
    (-0.5, -0.5),
    (-1.0, -1.0),
])
def test_execute(robot, elevator_default, hal_data, speed, ex_speed):
    robot.elevator = elevator_default
    met = MoveElevatorTime(robot, speed, 1.0, "CustomElevator", 15)
    met.initialize()
    met.execute()
    assert hal_data['pwm'][3]['value'] == ex_speed


@pytest.mark.parametrize("duration,speed,timeout,ex_speed", [
    (0.5, 0.5, 5.0, 0.5),
    (2.0, 1.0, 15.0, 1.0),
    # (5.0, 1.0, 1.0, 1.0, -1.0), # Timeouts don't seem to work in testing
])
def test_command_full(robot, elevator_default, hal_data, duration, speed, timeout, ex_speed):
    robot.elevator = elevator_default
    met = MoveElevatorTime(robot, speed, duration, "CustomElevator", timeout)
    sw = Stopwatch()
    met.initialize()
    sw.start()
    while not met.isFinished():
        met.execute()
        assert hal_data['pwm'][3]['value'] == ex_speed
    met.end()
    sw.stop()
    if duration < timeout:
        assert isclose(sw.elapsed_time_in_secs(), duration)
    else:
        # TODO: Timeouts don't seem to work in testing?
        assert isclose(sw.elapsed_time_in_secs(), timeout)