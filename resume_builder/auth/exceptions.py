class AuthenticationError(Exception):
    """Root exception for all auth-related errors."""
    pass


class UserNotFoundError(AuthenticationError):
    """Error raised when a user cannot be found using the provided lookup criteria."""
    pass


class UserAlreadyExistsError(AuthenticationError):
    """Error raised when trying to register a user with a username that is taken."""
    pass


class IncorrectPasswordError(AuthenticationError):
    """Error raised when trying to log in with an incorrect password."""
    pass


class InviteCodeNotFoundError(AuthenticationError):
    """Error raised when an invitation code cannot be found using the provided lookup criteria."""
    pass
