"""Package entry point; re-exports the public API."""

from .core import floor_log_b, IntegerLogarithmError

__all__ = ["floor_log_b", "IntegerLogarithmError"]
