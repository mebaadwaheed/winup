# This file will contain file system utilities.

import os
import shutil
import json
from pathlib import Path

def create_dir(path: str, exist_ok: bool = True):
    """Creates a directory, ignoring errors if it already exists by default."""
    os.makedirs(path, exist_ok=exist_ok)

def remove(path: str):
    """Removes a file or a directory (recursively)."""
    if os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.isfile(path):
        os.remove(path)

def copy(src: str, dest: str):
    """Copies a file or directory."""
    if os.path.isdir(src):
        shutil.copytree(src, dest)
    else:
        shutil.copy2(src, dest)

def move(src: str, dest: str):
    """Moves a file or directory."""
    shutil.move(src, dest)

def read_file(path: str) -> str:
    """Reads the content of a file as a string."""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path: str, content: str):
    """Writes a string to a file."""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def read_json(path: str) -> dict:
    """Reads and parses a JSON file."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_json(path: str, data: dict, indent: int = 4):
    """Writes a dictionary to a JSON file."""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent)

def exists(path: str) -> bool:
    """Checks if a file or directory exists."""
    return os.path.exists(path)

def list_dir(path: str = '.', recursive: bool = False) -> list[str]:
    """
    Lists the contents of a directory.
    
    Args:
        path (str): The directory path to list.
        recursive (bool): If True, lists files in all subdirectories as well.
        
    Returns:
        A list of paths for the files and directories found.
    """
    if not recursive:
        return [os.path.join(path, item) for item in os.listdir(path)]
    
    all_paths = []
    for root, _, files in os.walk(path):
        for name in files:
            all_paths.append(os.path.join(root, name))
    return all_paths 