from fractions import Fraction

import pytest
from days.day13.part1 import Part1


@pytest.mark.parametrize("a_start  ,b_start, a_speed, b_speed  ,a_cw,b_cw,expected", [
    (Fraction(19,20),Fraction(1,5),Fraction(1,20),Fraction(1,5),True,False,Fraction(5,20)),
    (Fraction(19,20),Fraction(1,5),Fraction(1,20),Fraction(1,5),True,True,Fraction(15,20)),
    (Fraction(19,20),Fraction(1,5),Fraction(1,20),Fraction(1,5),False,False,Fraction(5,20)),
    (Fraction(19,20),Fraction(1,5),Fraction(1,20),Fraction(1,5),False,True,Fraction(15,20)),
    (Fraction(19,20),Fraction(1,5),Fraction(1,20),Fraction(0),True,False,Fraction(5,20)),
    (Fraction(19,20),Fraction(1,5),Fraction(1,20),Fraction(0),True,True,Fraction(5,20)),
    (Fraction(19,20),Fraction(1,5),Fraction(1,20),Fraction(0),False,False,Fraction(15,20)),
    (Fraction(19,20),Fraction(1,5),Fraction(1,20),Fraction(0),False,True,Fraction(15,20)),
    (Fraction(19,20),Fraction(1,5),Fraction(0),Fraction(1,5),True,False,Fraction(5,20)),
    (Fraction(19,20),Fraction(1,5),Fraction(0),Fraction(1,5),True,True,Fraction(15,20)),
    (Fraction(19,20),Fraction(1,5),Fraction(0),Fraction(1,5),False,False,Fraction(5,20)),
    (Fraction(19,20),Fraction(1,5),Fraction(0),Fraction(1,5),False,True,Fraction(15,20)),
    

])
def test_calc_dist(a_start  ,b_start, a_speed, b_speed  ,a_cw,b_cw,expected):
    actual = Part1.calc_gap(a_start,b_start,a_speed, b_speed,a_cw,b_cw)
    assert actual == expected


@pytest.mark.parametrize("dist,a_speed, b_speed  ,a_cw,b_cw,expected", [
    (Fraction(5,20),Fraction(1,20),Fraction(1,5),True,False,1),
    (Fraction(15,20),Fraction(1,20),Fraction(1,5),True,True,5),
    (Fraction(5,20),Fraction(1,20),Fraction(1,5),False,False,Fraction(5,3)),
    (Fraction(15,20),Fraction(1,20),Fraction(1,5),False,True,3),
    (Fraction(5,20),Fraction(1,20),Fraction(0),True,False,5),
    (Fraction(5,20),Fraction(1,20),Fraction(0),True,True,5),
    (Fraction(15,20),Fraction(1,20),Fraction(0),False,False,15),
    (Fraction(15,20),Fraction(1,20),Fraction(0),False,True,15),
    (Fraction(5,20),Fraction(0),Fraction(1,5),True,False,Fraction(25,20)),
    (Fraction(15,20),Fraction(0),Fraction(1,5),True,True,Fraction(75,20)),
    (Fraction(5,20),Fraction(0),Fraction(1,5),False,False,Fraction(25,20)),
    (Fraction(15,20),Fraction(0),Fraction(1,5),False,True,Fraction(75,20)),

])
def test_time_to_pass(dist,a_speed, b_speed  ,a_cw,b_cw,expected):
    actual = Part1.time_to_pass(dist,a_speed, b_speed,a_cw,b_cw)
    assert actual == expected