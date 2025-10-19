from ..models import User, InviteCode
from .exceptions import UserAlreadyExistsError, UserNotFoundError, IncorrectPasswordError, InviteCodeNotFoundError, InviteCodeRedeemedError
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
        new_user.set_password(user_details.get("password"))
        self.db_session.add(new_user)
        self.db_session.commit()
        return new_user

    def register_user_with_invite_code(self, user_details: dict) -> User:
        invite_code = InviteCode.query.filter_by(code=user_details.get("invite_code")).first()
        if not invite_code:
            raise InviteCodeNotFoundError
        if invite_code.redeemed:
            raise InviteCodeRedeemedError
        existing = User.query.filter_by(username=user_details.get('username')).first()
        if existing:
            raise UserAlreadyExistsError

        new_user = User(username=user_details.get("username"))
        new_user.set_password(user_details.get("password"))

        invite_code.redeemed = True
        invite_code.user = new_user

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
