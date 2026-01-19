
from typing import Any


class UnauthorizedException(Exception):
    """Exception raised for unauthorized access."""
    def __init__(self, message: str = "Unauthorized access", details: Any = None):
        self.message = message
        self.details = details
        super().__init__(self.message)

class NotFoundException(Exception):
    """Exception raised when a resource is not found."""
    def __init__(self, message: str = "Resource not found", details: Any = None):
        self.message = message
        self.details = details
        super().__init__(self.message)
