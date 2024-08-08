import os
import bcrypt


class PasswordService:

    __SALT_ENV = "SALT"
    __SALT: bytes = None

    """ Lazily initialize the __SALT attribute by loading and encoding the environment variable specified by __SALT_ENV.
    Ensure it's only done once. Raise an error if the environment variable is not set."""
    @classmethod
    def get_salt(cls):
        if cls.__SALT is None:
            salt_value = os.getenv(cls.__SALT_ENV)
            if salt_value is None:
                raise ValueError(f"Environment variable {cls.__SALT_ENV} is not set.")
            cls.__SALT = salt_value.encode()
        return cls.__SALT

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hashpw(password.encode(), cls.get_salt()).decode('utf-8')

    @classmethod
    def check_password(cls, user_input: str, hashed_password: str) -> bool:
        result = bcrypt.checkpw(
            password=user_input.encode(),
            hashed_password=hashed_password.encode()
        )

        if not result:
            return False

        return True
