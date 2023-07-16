import argon2
from ..dal.dal_user import DalUser as Dal


class Hashing:
    @staticmethod
    def hash_password(pw: str):
        password = pw.encode(encoding='utf-8')  # Convert the password to bytes
        hashed_password = argon2.PasswordHasher().hash(password)

        return hashed_password

    @staticmethod
    def verify_password(email: str, pw: str):
        try:
            # Retrieve the hashed password from the database
            db_pw = Dal.GetPassword(email)

            if db_pw is not None:
                password = pw.encode(encoding='utf-8')  # Convert the password to bytes
                is_valid = argon2.PasswordHasher().verify(db_pw["password"], password)

                return is_valid
            else:
                return False

        except Exception:
            return False
