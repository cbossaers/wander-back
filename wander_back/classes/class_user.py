from ..logic.validator import Validator as Val
from email_validator import EmailNotValidError

class User:
    def __init__(self, name, email, password, picture=None):
        self._name = name
        self._email = email
        self._password = password
        self._picture = picture

    @property
    def name(self):
        return self._name

    # We check that the name variable is not empty
    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Name not provided.")
        self._name = value

    @property
    def email(self):
        return self._email

    # We check that the email variable is not empty and, if it isn't, that it has a valid email address format
    @email.setter
    def email(self, value):
        if not value:
            raise ValueError("Email not provided.")
        else:
            try:
                value = Val.validate_email(value)
            except EmailNotValidError:
                raise ValueError("Email is invalid.")
        
        self._email = value

    @property
    def password(self):
        return self._password

    # We check that the password variable is not empty and, if it isn't, that it conforms to pre-defined params
    @password.setter
    def password(self, value):
        if not value:
            raise ValueError("Password not provided.")
        else:
            try:
                value = Val.validate_password(value)
            except ValueError as e:
                raise e
        
        self._password = value

    @property
    def picture(self):
        return self._picture

    @picture.setter
    def picture(self, value):
        self._picture = value
