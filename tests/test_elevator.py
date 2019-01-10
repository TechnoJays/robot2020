import pytest
from subsystems.elevator import Elevator

"""
hal_data['pwm'] looks like this:
[{
    'zero_latch': False,
    'initialized': False,
    'raw_value': 0,
    'value': 0,
    'period_scale': None,
    'type': None
}, {
    'zero_latch': True,
    'initialized': True,
    'raw_value': 1011,
    'value': 0.0,
    'period_scale': 0,
    'type': 'talon'
},...]
"""


@pytest.fixture(scope="function")
def elevator_default(robot):
    return Elevator(robot, None, '../tests/test_configs/elevator_default.ini')


def isclose(a, b, rel_tol=0.1, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def test_elevator_default(elevator_default):
    assert elevator_default is not None
    assert elevator_default._motor is not None


def test_elevator_channel_4(robot, hal_data):
    elevtr = Elevator(robot, None, '../tests/test_configs/elevator_channel_4.ini')
    assert elevtr is not None
    assert elevtr._motor is not None
    assert hal_data['pwm'][4]['initialized'] is True
    assert hal_data['pwm'][4]['value'] == 0.0


def test_elevator_channel_5(robot, hal_data):
    elevtr = Elevator(robot, None, '../tests/test_configs/elevator_channel_5.ini')
    assert elevtr is not None
    assert elevtr._motor is not None
    assert hal_data['pwm'][5]['initialized'] is True
    assert hal_data['pwm'][5]['value'] == 0.0


@pytest.mark.parametrize("speed,ex_speed", [
    (0.0, 0.0),
    (0.5, 0.5),
    (1.0, 1.0),
    (-0.5, -0.5),
    (-1.0, -1.0),
])
def test_elevator_full_speed(robot, hal_data, speed, ex_speed):
    elevtr = Elevator(robot, None, '../tests/test_configs/elevator_default.ini')
    assert elevtr is not None
    assert elevtr._motor is not None
    elevtr.move_elevator(speed)
    assert hal_data['pwm'][3]['value'] == ex_speed


@pytest.mark.parametrize("speed,ex_speed", [
    (0.0, 0.0),
    (0.5, 0.25),
    (1.0, 0.5),
    (-0.5, -0.25),
    (-1.0, -0.5),
])
def test_elevator_scaled(robot, hal_data, speed, ex_speed):
    elevtr = Elevator(robot, None, '../tests/test_configs/elevator_scaled.ini')
    assert elevtr is not None
    assert elevtr._motor is not None
    elevtr.move_elevator(speed)
    assert hal_data['pwm'][3]['value'] == ex_speed


@pytest.mark.parametrize("current_count,speed,ex_speed", [
    (200, 0.0, 0.0),
    (0, 0.5, 0.5),
    (200, 1.0, 1.0),
    (550, 1.0, 0.0),
    (550, -0.5, -0.5),
    (200, -0.5, -0.5),
    (10, -1.0, 0.0),
])
def test_elevator_encoder_bounds(robot, hal_data, current_count, speed, ex_speed):
    elevtr = Elevator(robot, None, '../tests/test_configs/elevator_encoder_bounds.ini')
    assert elevtr is not None
    assert elevtr._motor is not None
    hal_data['encoder'][0]['count'] = current_count
    elevtr.move_elevator(speed)
    assert hal_data['pwm'][3]['value'] == ex_speed


def test_elevator_inverted(robot, hal_data):
    elevtr = Elevator(robot, None, '../tests/test_configs/elevator_inverted.ini')
    assert elevtr is not None
    assert elevtr._motor is not None
    assert hal_data['pwm'][3]['initialized'] is True
    assert hal_data['pwm'][3]['value'] == 0.0
    assert elevtr._motor.getInverted() is True


def test_elevator_disabled(robot):
    elevtr = Elevator(robot, None, '../tests/test_configs/elevator_disabled.ini')
    assert elevtr is not None
    assert elevtr._motor is None
