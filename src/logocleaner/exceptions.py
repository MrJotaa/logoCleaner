class LogoCleanerError(Exception):
    """Base exception for LogoCleaner errors."""


class InvalidMaskError(LogoCleanerError):
    """Raised when a strategy returns an invalid mask."""


class InvalidColorError(LogoCleanerError):
    """Raised when a color value is invalid."""


class UnsupportedModeError(LogoCleanerError):
    """Raised when an unsupported cleaning mode is requested."""
