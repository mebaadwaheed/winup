import functools
from . import profiler # Will point to the new web profiler

_cache = {}
_hits = 0
_misses = 0

def memo(func):
    """
    A memoization decorator for WinUp web components.
    
    Caches the component's output based on its arguments. If the component
    is called again with the same arguments, the cached HTML is returned
    instead of re-rendering it.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        global _hits, _misses
        
        try:
            key = (func, args, frozenset(kwargs.items()))
        except TypeError:
            key = (func, args, str(kwargs))

        if key in _cache:
            _hits += 1
            profiler.get_profiler().add_memo_hit()
            return _cache[key]
        
        _misses += 1
        profiler.get_profiler().add_memo_miss()
        result = func(*args, **kwargs)
        _cache[key] = result
        return result
        
    return wrapper

def clear_memo_cache():
    """Clears the entire memoization cache."""
    global _cache, _hits, _misses
    _cache.clear()
    _hits = 0
    _misses = 0
    # The profiler will also need a reset mechanism
    profiler.get_profiler().reset_memo_stats()
    print("Web memoization cache cleared.") 