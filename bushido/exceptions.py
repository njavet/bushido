
class UnitProcessingError(Exception):
    """Base exception for activity processing errors."""


class UnitProcessingWarning(Exception):
    """Raised when the input seems not correct."""


class InvalidUnitError(UnitProcessingError):
    """Raised when the input activity is invalid."""


class DatabaseError(UnitProcessingError):
    """Raised for database-related errors."""
