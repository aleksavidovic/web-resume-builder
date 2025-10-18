from ..models import User
from .exceptions import UserAlreadyExistsError

class AuthenticationService:
    def __init__(self, db_session):
        self.db_session = db_session

    def register_user(self, user_details: dict):
        """
        Creates a new user with provided details.
        Checks if username is taken.
        """
        existing = User.query.filter_by(username=user_details.username).first()
        if existing:
            raise UserAlreadyExistsError(f"ERROR: User with username `{user_details.username}` already exists.")
        new_user = User(username=user_details.username)
        if user_details.is_admin is not None:
            new_user.is_admin = user_details.is_admin
        new_user.set_password(user_details.password)
        self.db_session.add(user)
        self.db_session.commit()
        return new_user


