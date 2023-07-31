import os
import urllib.parse
from functools import reduce


def decode_filename(encoded_filename):
    """Decode special characters in directory or file names."""
    return urllib.parse.unquote(encoded_filename)


def get_directory_structure(rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir.
    """
    directory_structure = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        # Ignore hidden files and directories
        files = [f for f in files if not f[0] == "."]
        dirs[:] = [d for d in dirs if not d[0] == "."]

        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        parent = reduce(dict.get, folders[:-1], directory_structure)
        parent[folders[-1]] = subdir
    return directory_structure


def print_directory_structure(directory_structure, indent=0):
    """
    Prints the directory structure in a human-readable way.
    """
    for name, subdir in directory_structure.items():
        print("    " * indent + decode_filename(name))
        if isinstance(subdir, dict):
            print_directory_structure(subdir, indent + 1)


def main():
    directory_structure = get_directory_structure("./screencaps")
    print_directory_structure(directory_structure)


if __name__ == "__main__":
    main()
