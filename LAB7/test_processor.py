"""Hypothesis fuzz tests for all three attendance eligibility functions."""

import pytest
from hypothesis import given, strategies as st

from processor import attendance_percent, exam_eligibility, attendance_warning


# attendance_percent: valid-input properties

@given(
    total=st.integers(min_value=1, max_value=10000),
    attended=st.integers(min_value=0, max_value=10000),
    medical=st.integers(min_value=0, max_value=10000),
)
def test_attendance_percent_matches_crediting_rules(total, attended, medical):
    attended = min(attended, total)
    expected_credited = min(attended + min(medical, 5), total)
    assert attendance_percent(attended, total, medical) == (
        expected_credited * 100 // total
    )


@given(
    total=st.integers(min_value=1, max_value=10000),
    attended=st.integers(min_value=0, max_value=10000),
    medical=st.integers(min_value=0, max_value=10000),
)
def test_attendance_percent_is_between_zero_and_100(total, attended, medical):
    attended = min(attended, total)
    result = attendance_percent(attended, total, medical)
    assert 0 <= result <= 100


@given(total=st.integers(max_value=0))
def test_attendance_percent_rejects_nonpositive_total(total):
    with pytest.raises(ValueError, match="invalid total"):
        attendance_percent(0, total, 0)


@given(attended=st.integers(max_value=-1))
def test_attendance_percent_rejects_negative_attended(attended):
    with pytest.raises(ValueError, match="invalid attended"):
        attendance_percent(attended, 10, 0)


@given(extra=st.integers(min_value=1, max_value=10000))
def test_attendance_percent_rejects_attended_above_total(extra):
    with pytest.raises(ValueError, match="invalid attended"):
        attendance_percent(10 + extra, 10, 0)


@given(medical=st.integers(max_value=-1))
def test_attendance_percent_rejects_negative_medical_leave(medical):
    with pytest.raises(ValueError, match="invalid medical leave"):
        attendance_percent(5, 10, medical)


@pytest.mark.parametrize(
    "args",
    [
        (True, 10, 0),
        (1, False, 0),
        (1, 10, True),
        (1.5, 10, 0),
        ("1", 10, 0),
        (1, 10, None),
    ],
)
def test_attendance_percent_rejects_non_integer_arguments(args):
    with pytest.raises(TypeError):
        attendance_percent(*args)


# exam_eligibility: full decision table expressed as a property

@given(
    percent=st.integers(min_value=0, max_value=100),
    condonation=st.booleans(),
    fees=st.booleans(),
)
def test_exam_eligibility_decision_rules(percent, condonation, fees):
    if not fees:
        expected = "fees pending"
    elif percent >= 75:
        expected = "eligible"
    elif percent >= 65 and condonation:
        expected = "eligible"
    elif percent >= 65:
        expected = "condonation required"
    else:
        expected = "detained"

    assert exam_eligibility(percent, condonation, fees) == expected


@pytest.mark.parametrize("percent", [-1, 101])
def test_exam_eligibility_rejects_out_of_range_percentage(percent):
    with pytest.raises(ValueError, match="invalid attendance percentage"):
        exam_eligibility(percent, False, True)


@pytest.mark.parametrize("percent", [True, 75.0, "75", None])
def test_exam_eligibility_rejects_non_integer_percentage(percent):
    with pytest.raises(TypeError):
        exam_eligibility(percent, False, True)


@pytest.mark.parametrize(
    "condonation,fees",
    [(1, True), (False, 0), ("yes", True), (False, None)],
)
def test_exam_eligibility_requires_boolean_flags(condonation, fees):
    with pytest.raises(TypeError):
        exam_eligibility(75, condonation, fees)


# attendance_warning: all valid percentage/week combinations

@given(
    percent=st.integers(min_value=0, max_value=100),
    weeks=st.integers(min_value=0, max_value=10000),
)
def test_attendance_warning_decision_rules(percent, weeks):
    if percent >= 85:
        expected = None
    elif percent < 75 and weeks > 4:
        expected = "critical"
    elif percent < 75:
        expected = "final notice"
    else:
        expected = "reminder"

    assert attendance_warning(percent, weeks) == expected


@pytest.mark.parametrize("percent", [-1, 101])
def test_attendance_warning_rejects_out_of_range_percentage(percent):
    with pytest.raises(ValueError, match="invalid attendance percentage"):
        attendance_warning(percent, 5)


@given(weeks=st.integers(max_value=-1))
def test_attendance_warning_rejects_negative_weeks(weeks):
    with pytest.raises(ValueError, match="invalid weeks left"):
        attendance_warning(70, weeks)


@pytest.mark.parametrize(
    "percent,weeks",
    [(True, 5), (75.5, 5), ("75", 5), (75, False), (75, 1.5), (75, None)],
)
def test_attendance_warning_rejects_non_integer_arguments(percent, weeks):
    with pytest.raises(TypeError):
        attendance_warning(percent, weeks)
