"""Lab 7: hardened attendance eligibility processor.

The three public functions retain the valid-input behaviour of the Lab 6
attendance eligibility application.
"""


def _require_int(name, value):
    """Require an integer while deliberately rejecting bool values."""
    if type(value) is not int:
        raise TypeError(f"{name} must be an integer")


def _require_bool(name, value):
    """Require an actual bool rather than accepting arbitrary truthy values."""
    if type(value) is not bool:
        raise TypeError(f"{name} must be a boolean")


def attendance_percent(attended, total_classes, medical_leave_days):
    """Return credited attendance as an integer percentage.

    Medical leave is credited up to a maximum of five days. Credited
    attendance is capped at total_classes.
    """
    _require_int("attended", attended)
    _require_int("total_classes", total_classes)
    _require_int("medical_leave_days", medical_leave_days)

    if total_classes <= 0:
        raise ValueError("invalid total")
    if attended < 0 or attended > total_classes:
        raise ValueError("invalid attended")
    if medical_leave_days < 0:
        raise ValueError("invalid medical leave")

    credited_medical_leave = min(medical_leave_days, 5)
    credited = min(attended + credited_medical_leave, total_classes)
    return credited * 100 // total_classes


def exam_eligibility(percent, has_condonation, fees_paid):
    """Return the student's exam eligibility status."""
    _require_int("percent", percent)
    _require_bool("has_condonation", has_condonation)
    _require_bool("fees_paid", fees_paid)

    if percent < 0 or percent > 100:
        raise ValueError("invalid attendance percentage")

    if not fees_paid:
        return "fees pending"
    if percent >= 75:
        return "eligible"
    if percent >= 65:
        if has_condonation:
            return "eligible"
        return "condonation required"
    return "detained"


def attendance_warning(percent, weeks_left):
    """Return the appropriate attendance warning, or None."""
    _require_int("percent", percent)
    _require_int("weeks_left", weeks_left)

    if percent < 0 or percent > 100:
        raise ValueError("invalid attendance percentage")
    if weeks_left < 0:
        raise ValueError("invalid weeks left")

    if percent >= 85:
        return None
    if percent < 75:
        if weeks_left > 4:
            return "critical"
        return "final notice"
    return "reminder"


if __name__ == "__main__":
    # Small demonstration required by the Lab 7 handout.
    percentage = attendance_percent(30, 40, 0)
    print(f"Attendance percentage: {percentage}%")
    print(f"Exam eligibility: {exam_eligibility(percentage, False, True)}")
    print(f"Attendance warning: {attendance_warning(percentage, 5)}")
