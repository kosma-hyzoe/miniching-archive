import pytest
from context import core


def test_evaluate():
    assert core.evaluate("101010") == "64"
    assert core.evaluate("878889") == "3:1"
    assert core.evaluate("997877") == "10:5,6"
    assert core.evaluate("986779") == "26:1,4,6"
    assert core.evaluate("889996") == "32:1,2,3,4"
    assert core.evaluate("986699") == "41:1,2,3,4,6"
    assert core.evaluate("969996") == "50:1,2,3,4,5,6"
    assert core.evaluate("666666") == "2:s"
    assert core.evaluate("999999") == "1:s"


def test_get_reading():
    reading = core.get_reading("21:3,4", "...", "2022-12-30T14:02")
    assert reading["result"] == "21 -> 22"
