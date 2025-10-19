from ..models import User
from .exceptions import UserAlreadyExistsError, UserNotFoundError, IncorrectPasswordError
from flask_login import login_user

class AuthenticationService:
    def __init__(self, db_session):
        self.db_session = db_session

    def register_user(self, user_details: dict):
        """
        Creates a new user with provided details.
        Checks if username is taken.
        """
        existing = User.query.filter_by(username=user_details.get('username')).first()
        if existing:
            raise UserAlreadyExistsError(f"ERROR: User with username `{user_details.get('username')}` already exists.")
        new_user = User(username=user_details.get("username"))
        if user_details.get("is_admin") is not None:
            new_user.is_admin = user_details.get("is_admin")
        new_user.set_password(user_details.get("password"))
        self.db_session.add(new_user)
        self.db_session.commit()
        return new_user

    def login(self, user_credentials: dict):
        user = User.query.filter_by(username=user_credentials.get("username")).first()
        if user:
            if user.check_password(user_credentials.get("password")):
                login_user(user, remember=user_credentials.get("remember"))
                return user
            else:
                raise IncorrectPasswordError("ERROR: Incorrect Password Provided")
        else:
            raise UserNotFoundError(f"ERROR: No user found with provided username: {user_credentials.get('username')}")
