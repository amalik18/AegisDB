class DatabaseError(Exception):
    """Base class for database exceptions."""
    pass

class KeyNotFoundError(DatabaseError):
    """Raised when a key is not found in the database."""
    pass

class EncryptionError(Exception):
    """Raised when an encryption operation fails."""
    pass

class ConfigurationError(Exception):
    """Raised when there is a configuration issue."""
    pass