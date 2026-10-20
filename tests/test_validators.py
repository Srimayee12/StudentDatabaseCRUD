
import unittest

from app.validators import validate_student_data


class TestStudentValidation(unittest.TestCase):
    def test_valid_data(self):
        result = validate_student_data(
            "  srimayee  ",
            "  srimayee@example.com ",
            20,
            " Computer Science ",
        )

        self.assertEqual(
            result,
            ("srimayee", "srimayee@example.com", 20, "Computer Science"),
        )

    def test_empty_name(self):
        with self.assertRaises(ValueError):
            validate_student_data(
                "", "srimayee@example.com", 20, "Computer Science"
            )

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            validate_student_data(
                "srimayee", "invalid-email", 20, "Computer Science"
            )

    def test_invalid_age(self):
        for age in (0, -1, "abc", True):
            with self.subTest(age=age):
                with self.assertRaises(ValueError):
                    validate_student_data(
                        "srimayee",
                        "srimayee@example.com",
                        age,
                        "Computer Science",
                    )

    def test_empty_course(self):
        with self.assertRaises(ValueError):
            validate_student_data(
                "srimayee", "srimayee@example.com", 20, "  "
            )


if __name__ == "__main__":
    unittest.main()
