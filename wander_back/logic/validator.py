from email_validator import validate_email, EmailNotValidError
import re


class Validator:
    @staticmethod
    def validate_email(value: str):
        try:
            email_info = validate_email(value, check_deliverability=False)
            return email_info.normalized
        except EmailNotValidError:
            raise

    @staticmethod
    def validate_password(value: str):
        min_length = 12

        if len(value) < min_length:
            raise ValueError(100)
        if not re.search(r"[A-Z]", value):
            raise ValueError(101)
        if not re.search(r"[a-z]", value):
            raise ValueError(102)
        if not re.search(r"\d", value):
            raise ValueError(103)
        if not re.search(r"[!@#*_+\-?.]", value):
            raise ValueError(104)

        return value

    @staticmethod
    def author_exists(value):
        return value

    @staticmethod
    def period_is_valid(value):
        valid_periods = ["Spring", "Summer", "Autumn", "Winter"]
        if value in valid_periods:
            return value
        else:
            raise Exception("Invalid period")

    @staticmethod
    def itinerary_exists(value):
        return value
