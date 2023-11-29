from acp_times import open_time, close_time
import arrow
import nose  # Testing framework
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.WARNING)
log = logging.getLogger(__name__)

def test_open_time_control_dist_set_0():
    start_time = arrow.get('2023-11-09T00:00')
    open_time_0 = open_time(0, 200, start_time)
    assert open_time_0 == start_time

def test_open_time_regular_cases():
    start_time = arrow.get('2023-11-09T00:00')
    nose.tools.assert_equal(open_time(150, 200, start_time), start_time.shift(minutes=+265))
    nose.tools.assert_equal(open_time(300, 300, start_time), start_time.shift(minutes=+540))
    nose.tools.assert_equal(open_time(500, 600, start_time), start_time.shift(minutes=+928))

def test_open_time_edge_cases():
    start_time = arrow.get('2023-11-09T00:00')
    nose.tools.assert_equal(open_time(0, 200, start_time), start_time)
    nose.tools.assert_equal(open_time(40, 200, start_time), start_time.shift(minutes=+71))

def test_close_time_regular_cases():
    start_time = arrow.get('2023-11-09T00:00')
    nose.tools.assert_equal(close_time(150, 200, start_time), start_time.shift(minutes=+600))
    nose.tools.assert_equal(close_time(500, 600, start_time), start_time.shift(minutes=+2000))
    nose.tools.assert_equal(close_time(300, 300, start_time), start_time.shift(minutes=+1200))

def test_close_time_edge_cases():
    start_time = arrow.get('2023-11-09T00:00')
    nose.tools.assert_equal(close_time(0, 200, start_time), start_time.shift(minutes=+60))
