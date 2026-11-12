
def normalize_srn(srn):
    """
    Trims and upper-cases a student registration number.
    Handles invalid input safely.
    """
    if not isinstance(srn, str):
        return ""

    return srn.strip().replace(' ', '').upper()


def attendance_from_ratio(text):
    """
    Converts ATTENDED/HELD into a whole-number percentage.
    Handles malformed input and prevents division by zero.
    """
    if not isinstance(text, str):
        return 0

    try:
        parts = text.split('/')

        if len(parts) != 2:
            return 0

        attended = int(parts[0].strip())
        held = int(parts[1].strip())

        if attended < 0 or held <= 0:
            return 0

        return attended * 100 // held

    except (ValueError, TypeError, OverflowError):
        return 0


def attendance_from_register(marks):
    """
    Calculates attendance from P (present) and A (absent).
    Handles empty and invalid input safely.
    """
    if not isinstance(marks, str):
        return 0

    marks = marks.strip().upper()

    if not marks:
        return 0

    if any(mark not in ('P', 'A') for mark in marks):
        return 0

    return marks.count('P') * 100 // len(marks)


def main():
    print("==== Running normalize_srn ====")
    value = input("Enter an SRN (e.g. pes1ug23cs001): ")
    print("Normalized SRN:", normalize_srn(value))

    print("\n==== Running attendance_from_ratio ====")
    value = input("Enter classes attended and held as ATTENDED/HELD (e.g. 30/40): ")
    print("Attendance percent:", attendance_from_ratio(value))

    print("\n==== Running attendance_from_register ====")
    value = input("Enter the register as P/A marks (e.g. PPAPP): ")
    print("Attendance percent:", attendance_from_register(value))


if __name__ == "__main__":
    main()
