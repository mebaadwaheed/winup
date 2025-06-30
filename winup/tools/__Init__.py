from .wintools import wintools as wintools_singleton
from .profiler import profiler as profiler_singleton

wintools = wintools_singleton
profiler = profiler_singleton

from . import notifications

__all__ = ["wintools", "profiler", "notifications"]
