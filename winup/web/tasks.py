import asyncio
from functools import wraps
from typing import Callable, Optional, Any

class TaskManager:
    """
    A web-specific task manager that runs functions in the background
    using asyncio.
    """
    def run(
        self,
        on_start: Optional[Callable[[], Any]] = None,
        on_finish: Optional[Callable[[Any], Any]] = None,
        on_error: Optional[Callable[[Exception], Any]] = None,
    ):
        """
        A decorator that runs a function as a background asyncio task.

        Args:
            on_start: An async or sync function to call before the task starts.
            on_finish: An async or sync function to call when the task succeeds.
                       It receives the task's return value.
            on_error: An async or sync function to call if the task fails.
                      It receives the exception object.
        """
        def decorator(func: Callable):
            @wraps(func)
            async def wrapper(*args, **kwargs):

                async def task_runner():
                    # --- on_start ---
                    if on_start:
                        if asyncio.iscoroutinefunction(on_start):
                            await on_start()
                        else:
                            on_start()
                    
                    try:
                        # --- Run the actual user function ---
                        # If the user function is async, await it. Otherwise, run it
                        # in a thread to avoid blocking the event loop.
                        if asyncio.iscoroutinefunction(func):
                            result = await func(*args, **kwargs)
                        else:
                            loop = asyncio.get_running_loop()
                            result = await loop.run_in_executor(None, lambda: func(*args, **kwargs))

                        # --- on_finish ---
                        if on_finish:
                            if asyncio.iscoroutinefunction(on_finish):
                                await on_finish(result)
                            else:
                                on_finish(result)
                    
                    except Exception as e:
                        # --- on_error ---
                        if on_error:
                            if asyncio.iscoroutinefunction(on_error):
                                await on_error(e)
                            else:
                                on_error(e)
                        else:
                            # If no error handler, at least log the error
                            print(f"Task '{func.__name__}' failed with an unhandled exception: {e}")

                # Schedule the task to run in the background
                asyncio.create_task(task_runner())

            return wrapper
        return decorator

# Create a singleton instance for easy access, e.g., `@tasks.run()`
tasks = TaskManager()
run = tasks.run 