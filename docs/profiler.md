# Performance Profiler

WinUp includes a simple, built-in profiler that helps you measure the execution time of your functions. This is useful for identifying performance bottlenecks in your application without needing to add complex timing logic manually.

The global `winup.profiler` object is a singleton instance of the `Profiler` class.

## How to Use It

The profiler works as a decorator that you can apply to any function.

```python
from winup import profiler

@profiler.measure()
def my_long_running_function():
    # ... some slow code ...
    pass

@profiler.measure(func_name="CustomNameForUI.update")
def another_function():
    # ...
    pass
```

### `@profiler.measure()`

When you decorate a function with `@profiler.measure()`, the profiler will:
1.  Record the time just before the function is executed.
2.  Execute the function.
3.  Record the time just after the function completes.
4.  Calculate the difference in milliseconds.
5.  Print the result to the console and store it for later retrieval.

You can optionally pass a `func_name` to the decorator. If you don't, the name of the function itself will be used as the key.

## Viewing Results

The profiler automatically prints the execution time of each profiled function as it runs.

To see a summary of all measurements taken during the application's lifetime, you can call `profiler.print_results()`.

```python
from winup import profiler

# After running your app...
profiler.print_results()
```

This will output a summary to the console:

```
--- Performance Profile ---
- my_long_running_function: 256.1234 ms
- CustomNameForUI.update: 12.5678 ms

--- Memoization Cache ---
- Hits: 150
- Misses: 12
- Hit Ratio: 92.59%
-------------------------
```

## Integration with Memoization

The profiler also automatically tracks hits and misses for the `@memo` decorator (WinUp's memoization system). This data is included in the `print_results()` output, giving you a clear picture of how effective your caching strategy is. 