from app.database import get_connection
from app.validators import validate_student_data


def create_student(name, email, age, course):
    """Add a validated student to the database."""
    name, email, age, course = validate_student_data(
        name, email, age, course
    )
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO students (name, email, age, course)
            VALUES (?, ?, ?, ?)
            """,
            (name, email, age, course),
        )
        return cursor.lastrowid


def get_all_students():
    """Return all students, ordered by their ID."""
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM students ORDER BY id"
        ).fetchall()
        return [dict(row) for row in rows]


def get_student_by_id(student_id):
    """Return one student by ID, or None if not found."""
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,),
        ).fetchone()
        return dict(row) if row else None



def update_student(student_id, name, email, age, course):
    """Update an existing student's details."""

    name, email, age, course = validate_student_data(
        name, email, age, course
    )

    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE students
            SET name = ?, email = ?, age = ?, course = ?
            WHERE id = ?
            """,
            (
                name,
                email,
                age,
                course,
                student_id,
            ),
        )
        return cursor.rowcount > 0



def delete_student(student_id):
    """Delete a student by ID."""
    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,),
        )
        return cursor.rowcount > 0