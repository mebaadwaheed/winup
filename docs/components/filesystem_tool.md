# Filesystem Tool

The `winup.tools.filesystem` module provides a simple, cross-platform API for common file operations.

```python
from winup.tools import filesystem

# Create a directory
filesystem.create_dir("my_app_data")

# Write to a file
filesystem.write_file("my_app_data/config.txt", "Hello, World!")

# Read from a file
content = filesystem.read_file("my_app_data/config.txt") # "Hello, World!"

# Work with JSON
data = {"theme": "dark", "version": 1}
filesystem.write_json("my_app_data/settings.json", data)
settings = filesystem.read_json("my_app_data/settings.json")

# Check if a file exists
if filesystem.exists("my_app_data/settings.json"):
    print("Settings file found!")

# Clean up
filesystem.remove("my_app_data")
```