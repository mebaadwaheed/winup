# Web Profiler & Memoization

WinUp for Web includes built-in tools to help you optimize your application's performance. These include a profiler for measuring code execution time and a memoization decorator for caching the results of expensive functions.

## Profiler

The web profiler allows you to measure how long specific functions take to execute. The results are collected on the server and can be viewed by navigating to a special URL.

### How to Use It

1.  **Import the profiler**: `from winup import web`
2.  **Decorate your function**: Apply the `@web.profiler.get_profiler().measure("unique_name")` decorator to any function you want to measure.
3.  **View the results**: Run your app and navigate to `http://127.0.0.1:8000/_winup/profiler`.

The results will be displayed as a JSON object in your browser.

```python
from winup import web

@web.profiler.get_profiler().measure("my_complex_calculation")
def my_complex_calculation():
    # ... some long-running code ...
    return "done"
```

When you call `my_complex_calculation()`, the profiler will record its execution time. The JSON output will look something like this:
```json
{
  "measurements": {
    "my_complex_calculation": "100.2345 ms"
  },
  "memoization": { ... }
}
```

## Memoization

Memoization is a powerful caching technique. When you "memoize" a component, WinUp stores the rendered HTML output. If the component is called again with the exact same arguments, WinUp returns the cached HTML instantly instead of re-rendering the component, which can provide a significant speed boost.

### How to Use It

Apply the `@web.memo.memo` decorator to your component functions. It's important to place it **above** the `@web.component` decorator.

```python
from winup import web

@web.memo.memo
@web.component
def UserAvatar(username: str):
    """A potentially expensive component to render."""
    # ... logic to get user avatar URL ...
    return web.ui.Image(src=f"/avatars/{username}.png")

# --- In another component ---
def UserList():
    return web.ui.Column(children=[
        # The first call renders the component and caches the result.
        UserAvatar(username="alice"),
        
        # This call is a "cache hit". The stored HTML is returned instantly.
        UserAvatar(username="alice"),

        # This call has different arguments, so it's a "cache miss".
        # It will be rendered and its result will be added to the cache.
        UserAvatar(username="bob"),
    ])
```

### Integration with Profiler

The memoization system is automatically integrated with the profiler. The `/_winup/profiler` endpoint will show you statistics about your cache performance, including:
- `hits`: The number of times a cached result was successfully used.
- `misses`: The number of times a component had to be rendered because it wasn't in the cache.
- `hit_ratio_percent`: The percentage of cache hits, a key indicator of your caching strategy's effectiveness. 