# Memoization

Memoization is a powerful optimization technique used to speed up applications by caching the results of expensive function calls and returning the cached result when the same inputs occur again. In WinUp, this is particularly useful for components that are rendered frequently with the same properties.

WinUp provides a simple `@memo` decorator to enable memoization on any component or function.

## How to Use It

Simply import `memo` from `winup` and apply it as a decorator to your component function.

```python
from winup import memo, ui

@memo
@winup.component
def UserProfile(name: str, avatar_url: str):
    """
    A component that might be expensive to render, especially if the
    avatar image involves network requests or complex processing.
    """
    return ui.Row(children=[
        ui.Image(src=avatar_url),
        ui.Label(text=name)
    ])

# --- In your main application ---

# The first time this is called, the UserProfile component will be
# fully rendered and its resulting widget will be cached.
UserProfile(name="Alice", avatar_url="path/to/alice.png")

# The second time, with the exact same arguments, the cached widget
# is returned almost instantly, skipping the entire render process.
UserProfile(name="Alice", avatar_url="path/to/alice.png") 

# This call has a different 'name', so it will trigger a new render
# and a new entry in the cache.
UserProfile(name="Bob", avatar_url="path/to/bob.png")
```

## How It Works

The `@memo` decorator wraps your function and creates a unique **cache key** based on the function's name and the arguments (`args` and `kwargs`) it was called with.

- **Cache Hit:** If the key is found in the cache, the stored result (the previously rendered widget) is returned immediately. This is a "hit".
- **Cache Miss:** If the key is not found, the original function is executed, and its result is stored in the cache before being returned. This is a "miss".

The `@memo` decorator is smart enough to handle unhashable arguments like dictionaries (which are common in `props`) by converting them to a stable string representation for the cache key.

## Cache Invalidation

The cache is persistent for the lifetime of the application. If you need to manually clear it, you can call `clear_memo_cache()`.

```python
from winup import clear_memo_cache

# This will completely empty the cache for all memoized functions.
clear_memo_cache()
```
This can be useful in development or if you know that the underlying data used by your components has changed in a way that the arguments do not reflect.

## Monitoring Performance

The `@memo` decorator is integrated with the `winup.profiler`. When you print the profiler results, you will see a summary of memoization hits and misses, allowing you to see how effective your caching strategy is. 