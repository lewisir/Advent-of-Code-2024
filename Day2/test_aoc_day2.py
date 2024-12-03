# Tests for Day 2

import pytest
import aoc_day2


def test_check_in_range():
    assert aoc_day2.check_in_range(0) == False


def test_check_report():
    assert aoc_day2.check_report([1, 2, 3, 4], True) == True
    assert aoc_day2.check_report([1, 2, 3, 1], True) == True
    assert aoc_day2.check_report([4, 2, 3, 4], True) == True
