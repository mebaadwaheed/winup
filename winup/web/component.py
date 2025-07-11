import functools

def component(func):
    """
    A decorator to mark a function as a web component.
    For now, it's a simple pass-through. In the future, it can be
    extended to add web-specific lifecycle hooks or other functionality.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper 