import math

import pytest
from days.day13.part1 import Part1


@pytest.mark.parametrize("a_start  ,b_start, a_speed, b_speed  ,a_cw,b_cw,expected", [
    (19/20,1/5,1/20,1/5,True,False,5/20),
    (19/20,1/5,1/20,1/5,True,True,15/20),
    (19/20,1/5,1/20,1/5,False,False,5/20),
    (19/20,1/5,1/20,1/5,False,True,15/20),

])
def test_calc_dist(a_start  ,b_start, a_speed, b_speed  ,a_cw,b_cw,expected):
    assert Part1.calc_gap(a_start,b_start,a_speed, b_speed,a_cw,b_cw) == expected


@pytest.mark.parametrize("dist,a_speed, b_speed  ,a_cw,b_cw,expected", [
    (5/20,1/20,1/5,True,False,1),
    (15/20,1/20,1/5,True,True,5),
    (5/20,1/20,1/5,False,False,5/3),
    (15/20,1/20,1/5,False,True,3),

])
def test_time_to_pass(dist,a_speed, b_speed  ,a_cw,b_cw,expected):
    actual = Part1.time_to_pass(dist,a_speed, b_speed,a_cw,b_cw) == expected
    print(actual,expected)
    assert math.isclose(actual,expected) == True