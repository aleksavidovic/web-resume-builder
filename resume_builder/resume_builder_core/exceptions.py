class ApplicationException(Exception):
    """ Base exception for this application """
    pass

class EntryNotFoundError(ApplicationException):
    """ Raised when a database entry is not found. """
    pass

class AuthorizationError(ApplicationException):
    """ Raised when a user is not authorized to perform an action. """
    pass
