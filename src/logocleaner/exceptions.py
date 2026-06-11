class LogoCleanerError(Exception):
    """Base exception for LogoCleaner errors."""


class InvalidMaskError(LogoCleanerError):
    """Raised when a strategy returns an invalid mask."""


class InvalidColorError(LogoCleanerError):
    """Raised when a color value is invalid."""


class UnsupportedModeError(LogoCleanerError):
    """Raised when an unsupported cleaning mode is requested."""


class BackgroundColorDetectionError(LogoCleanerError):
    """Raised when automatic background color detection fails."""


class InvalidToleranceError(LogoCleanerError):
    """Raised when a tolerance value is invalid."""


class ImageLoadError(LogoCleanerError):
    """Raised when an image cannot be loaded."""


class ImageSaveError(LogoCleanerError):
    """Raised when an image cannot be saved."""
