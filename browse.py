import streamlit as st
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
        subdir = dict.fromkeys(dirs)
        parent = reduce(dict.get, folders[:-1], directory_structure)
        parent[folders[-1]] = subdir
    return directory_structure


def get_label(level, directory_structure):
    """Determine label based on directory content."""
    labels = [
        "Player Type",
        "Player Brand/Model",
        "Player Settings",
        "Player Output/Resolution",
        "Processor Brand/Model",
        "Processor Settings",
        "Processor Output/Resolution",
    ]
    if level < len(labels):
        return labels[level]
    else:
        # The "Processor" labels are repeated for each processor.
        # We determine the processor number by counting the number of "Processor Output/Resolution" directories.
        processor_number = (
            sum("Processor Output/Resolution" in path for path in directory_structure)
            + 1
        )
        return f"Processor {processor_number} {labels[level % len(labels)]}"


def display_dropdowns(directory_structure, parent="", level=0):
    """Display dropdowns for the directory structure."""
    for name, subdir in directory_structure.items():
        decoded_name = decode_filename(name)
        if isinstance(subdir, dict):
            choices = list(subdir.keys())
            if choices:
                label = get_label(level, directory_structure)
                selected_encoded_option = st.selectbox(label, choices)
                selected_option = decode_filename(selected_encoded_option)
                display_dropdowns(
                    subdir[selected_encoded_option],
                    f"{parent}/{decoded_name}/{selected_option}",
                    level + 1,
                )


st.title("File Selector")

directory_structure = get_directory_structure("./screencaps")
display_dropdowns(directory_structure)
