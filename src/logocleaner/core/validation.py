from __future__ import annotations

import math
from numbers import Real

from logocleaner.exceptions import InvalidToleranceError


def validate_tolerance(value: object) -> float:
    """Validate and return a color distance tolerance."""

    if isinstance(value, bool) or not isinstance(value, Real):
        raise InvalidToleranceError("Tolerance must be a number.")

    tolerance = float(value)

    if not math.isfinite(tolerance):
        raise InvalidToleranceError("Tolerance must be a finite number.")

    if tolerance < 0:
        raise InvalidToleranceError("Tolerance must be >= 0.")

    return tolerance
