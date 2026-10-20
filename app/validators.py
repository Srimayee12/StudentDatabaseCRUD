
import re


def validate_student_data(name, email, age, course):
    """Validate student fields before database operations."""

    if not isinstance(name, str) or not name.strip():
        raise ValueError("Student name cannot be empty.")

    if not isinstance(email, str) or not email.strip():
        raise ValueError("Email cannot be empty.")

    email = email.strip().lower()
    email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    if not re.fullmatch(email_pattern, email):
        raise ValueError("Please enter a valid email address.")

    if isinstance(age, bool):
        raise ValueError("Age must be a positive integer.")

    try:
        age = int(age)
    except (ValueError, TypeError):
        raise ValueError("Age must be a positive integer.")

    if age <= 0:
        raise ValueError("Age must be greater than zero.")

    if not isinstance(course, str) or not course.strip():
        raise ValueError("Course cannot be empty.")

    return name.strip(), email, age, course.strip()
