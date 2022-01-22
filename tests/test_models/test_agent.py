"""test_agent.py

Tests the Agent model. All tests rely on the pytest fixture
crash_dump_50, an Agent initialized with 100G of total storage
and 50G of currently used storage.
"""
import pytest

from diskspacemonitor.models import Agent
import diskspacemonitor.warn as warn


def test_storage_limit_101_percent_invalid(crash_dump_50: Agent) -> bool:
    with pytest.raises(warn.StorageLimitOutOfRangeError):
        crash_dump_50.set_storage_limit(101)


def test_current_storage_useage_over_limit(crash_dump_50: Agent) -> bool:
    with pytest.raises(warn.OverMemoryLimitError):
        crash_dump_50.set_storage_limit(90)
        crash_dump_50.set_current_storage_useage(91)


@pytest.mark.parametrize(
    "test_input,expected", [(55, 55), (30, 30), (15, 15), (90, 90), (1, 1)]
)
def test_current_storage_useage_change(
    test_input: int, expected: int, crash_dump_50: Agent
) -> bool:
    crash_dump_50.set_current_storage_useage(test_input)

    actual = crash_dump_50.current_storage_useage

    assert actual == expected


@pytest.mark.parametrize(
    "test_input,expected", [(55, 45), (30, 70), (15, 85), (90, 10), (1, 99)]
)
def test_free_storage_change(
    test_input: int, expected: int, crash_dump_50: Agent
) -> bool:
    crash_dump_50.set_current_storage_useage(test_input)

    actual = crash_dump_50.free_storage

    assert actual == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [(55, 55.0), (30, 30.0), (15, 15.0), (90, 90.0), (1, 1.0)],
)
def test_proportion_of_storage_used_change(
    test_input: int,
    expected: int,
    crash_dump_50: Agent,
) -> bool:
    crash_dump_50.set_current_storage_useage(test_input)

    actual = crash_dump_50.proportion_of_total_storage_used

    assert actual - expected < 0.00001
