class AuthenticationError(Exception):
    """Root exception for all auth-related errors."""

    pass


class UserNotFoundError(AuthenticationError):
    """Error raised when a user cannot be found using the provided lookup criteria."""

    pass
