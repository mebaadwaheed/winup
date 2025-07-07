import time
import functools
from threading import Lock

class Profiler:
    """
    A thread-safe profiler for the web backend to measure performance
    and track memoization statistics.
    """
    def __init__(self):
        self._lock = Lock()
        self.reset()

    def reset(self):
        """Resets all profiling statistics to their initial state."""
        with self._lock:
            self._results = {}
            self._memo_hits = 0
            self._memo_misses = 0

    def reset_memo_stats(self):
        """Resets only the memoization statistics."""
        with self._lock:
            self._memo_hits = 0
            self._memo_misses = 0

    def add_memo_hit(self):
        with self._lock:
            self._memo_hits += 1

    def add_memo_miss(self):
        with self._lock:
            self._memo_misses += 1
            
    def measure(self, name: str):
        """A decorator to measure the execution time of a function."""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.perf_counter()
                result = func(*args, **kwargs)
                end_time = time.perf_counter()
                execution_time_ms = (end_time - start_time) * 1000
                
                with self._lock:
                    self._results[name] = f"{execution_time_ms:.4f} ms"
                return result
            return wrapper
        return decorator

    def get_results(self) -> dict:
        """Returns a dictionary of all recorded profiling results."""
        with self._lock:
            total_lookups = self._memo_hits + self._memo_misses
            hit_ratio = (self._memo_hits / total_lookups * 100) if total_lookups > 0 else 0
            
            return {
                "measurements": self._results.copy(),
                "memoization": {
                    "hits": self._memo_hits,
                    "misses": self._memo_misses,
                    "total_lookups": total_lookups,
                    "hit_ratio_percent": round(hit_ratio, 2),
                }
            }

_profiler_instance = Profiler()

def get_profiler() -> Profiler:
    """Returns the singleton profiler instance."""
    return _profiler_instance 