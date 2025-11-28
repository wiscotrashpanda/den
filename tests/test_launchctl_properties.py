"""Property-based tests for the launchctl helper module.

These tests use Hypothesis to verify universal properties across all inputs
for the launchctl validator functions.
"""

from hypothesis import given, settings, strategies as st

from den.launchctl_validator import (
    validate_task_name,
    validate_interval,
    validate_hour,
    validate_minute,
)


# Strategies for generating test data
valid_task_name_chars = st.text(
    alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-",
    min_size=1,
)

# Characters that should be rejected in task names
invalid_task_name_chars = st.text(
    alphabet=" /\\!@#$%^&*()+=[]{}|;:'\",.<>?`~",
    min_size=1,
)


@settings(max_examples=100)
@given(name=valid_task_name_chars)
def test_property_valid_task_names_accepted(name: str):
    """**Feature: launchctl-helper, Property 7: Task Name Character Validation**

    *For any* string containing only alphanumeric characters, hyphens, and
    underscores, the validator should accept it.

    **Validates: Requirements 6.2**
    """
    is_valid, error_msg = validate_task_name(name)
    assert is_valid is True, f"Valid task name '{name}' was rejected: {error_msg}"
    assert error_msg == ""


@settings(max_examples=100)
@given(name=invalid_task_name_chars)
def test_property_invalid_task_names_rejected(name: str):
    """**Feature: launchctl-helper, Property 7: Task Name Character Validation**

    *For any* string containing spaces, slashes, or special characters
    (other than hyphens and underscores), the task name validator should reject it.

    **Validates: Requirements 6.2**
    """
    is_valid, error_msg = validate_task_name(name)
    assert is_valid is False, f"Invalid task name '{name}' was accepted"
    assert error_msg != ""


@settings(max_examples=100)
@given(seconds=st.integers(max_value=0))
def test_property_non_positive_intervals_rejected(seconds: int):
    """**Feature: launchctl-helper, Property 8: Interval Validation**

    *For any* integer less than or equal to zero, the interval validator
    should reject it.

    **Validates: Requirements 6.4**
    """
    is_valid, error_msg = validate_interval(seconds)
    assert is_valid is False, f"Non-positive interval {seconds} was accepted"
    assert error_msg != ""


@settings(max_examples=100)
@given(seconds=st.integers(min_value=1))
def test_property_positive_intervals_accepted(seconds: int):
    """**Feature: launchctl-helper, Property 8: Interval Validation**

    *For any* positive integer, the interval validator should accept it.

    **Validates: Requirements 6.4**
    """
    is_valid, error_msg = validate_interval(seconds)
    assert is_valid is True, f"Positive interval {seconds} was rejected: {error_msg}"
    assert error_msg == ""


@settings(max_examples=100)
@given(hour=st.integers(min_value=0, max_value=23))
def test_property_valid_hours_accepted(hour: int):
    """**Feature: launchctl-helper, Property 9: Hour Validation**

    *For any* integer in the range 0-23, the hour validator should accept it.

    **Validates: Requirements 6.5**
    """
    is_valid, error_msg = validate_hour(hour)
    assert is_valid is True, f"Valid hour {hour} was rejected: {error_msg}"
    assert error_msg == ""


@settings(max_examples=100)
@given(hour=st.integers().filter(lambda x: x < 0 or x > 23))
def test_property_invalid_hours_rejected(hour: int):
    """**Feature: launchctl-helper, Property 9: Hour Validation**

    *For any* integer outside the range 0-23, the hour validator should reject it.

    **Validates: Requirements 6.5**
    """
    is_valid, error_msg = validate_hour(hour)
    assert is_valid is False, f"Invalid hour {hour} was accepted"
    assert error_msg != ""


@settings(max_examples=100)
@given(minute=st.integers(min_value=0, max_value=59))
def test_property_valid_minutes_accepted(minute: int):
    """**Feature: launchctl-helper, Property 10: Minute Validation**

    *For any* integer in the range 0-59, the minute validator should accept it.

    **Validates: Requirements 6.6**
    """
    is_valid, error_msg = validate_minute(minute)
    assert is_valid is True, f"Valid minute {minute} was rejected: {error_msg}"
    assert error_msg == ""


@settings(max_examples=100)
@given(minute=st.integers().filter(lambda x: x < 0 or x > 59))
def test_property_invalid_minutes_rejected(minute: int):
    """**Feature: launchctl-helper, Property 10: Minute Validation**

    *For any* integer outside the range 0-59, the minute validator should reject it.

    **Validates: Requirements 6.6**
    """
    is_valid, error_msg = validate_minute(minute)
    assert is_valid is False, f"Invalid minute {minute} was accepted"
    assert error_msg != ""
