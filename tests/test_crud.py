import unittest

from app.crud import (
    create_student,
    get_all_students,
    get_student_by_id,
    update_student,
    delete_student,
)


class TestStudentCRUD(unittest.TestCase):
    def test_create_and_read_student(self):
        student_id = create_student(
            "Test Student",
            "test.student@example.com",
            20,
            "Computer Science",
        )

        student = get_student_by_id(student_id)

        self.assertIsNotNone(student)
        self.assertEqual(student["name"], "Test Student")
        self.assertEqual(student["email"], "test.student@example.com")

        # Clean up the test record.
        delete_student(student_id)

    def test_update_student(self):
        student_id = create_student(
            "Original Name",
            "original@example.com",
            21,
            "Mathematics",
        )

        updated = update_student(
            student_id,
            "Updated Name",
            "updated@example.com",
            22,
            "Physics",
        )

        self.assertTrue(updated)

        student = get_student_by_id(student_id)
        self.assertEqual(student["name"], "Updated Name")
        self.assertEqual(student["age"], 22)

        delete_student(student_id)

    def test_delete_student(self):
        student_id = create_student(
            "Delete Me",
            "delete.me@example.com",
            19,
            "Engineering",
        )

        self.assertTrue(delete_student(student_id))
        self.assertIsNone(get_student_by_id(student_id))

    def test_get_all_students(self):
        student_id = create_student(
            "List Test",
            "list.test@example.com",
            20,
            "Biology",
        )

        students = get_all_students()

        self.assertTrue(
            any(student["id"] == student_id for student in students)
        )

        delete_student(student_id)


if __name__ == "__main__":
    unittest.main()