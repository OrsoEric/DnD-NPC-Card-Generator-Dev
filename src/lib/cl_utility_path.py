"""
Utility functions for handling file paths in a cross-platform manner.

This module provides utilities for converting lists of path components
into properly formatted OS-specific paths.
"""

import logging
from pathlib import Path
from typing import List

def convert_to_path(
    i_ls_path_components: List[str]
) -> Path:
    """
    Convert a list of path components into a cross-platform Path object.

    This function takes a list of string path components and converts them
    into a properly formatted Path object that is compatible with the
    operating system's path conventions.

    Parameters
    ----------
    i_ls_path_components : List[str]
        A list of path components to be joined into a single path.
        Each component should be a string representing a part of the path.

    Returns
    -------
    Path
        A pathlib.Path object representing the joined path components.

    Examples
    --------
    >>> convert_to_path(["src", "data", "file.json"])
    PosixPath('src/data/file.json')  # On Unix-like systems

    >>> convert_to_path(["C:", "Users", "Documents", "file.txt"])
    WindowsPath('C:\\\\Users\\\\Documents\\\\file.txt')  # On Windows
    """
    
    # Create a Path object from the list of components
    cl_path: Path = Path(*i_ls_path_components)
    
    return cl_path


# Example usage for testing purposes
if __name__ == "__main__":
    # Basic path conversion
    test_components = ["src", "data", "test.json"]
    result_path = convert_to_path(test_components)
    print(f"Converted path: {result_path}")
