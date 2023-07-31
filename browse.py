import os
import urllib.parse
import streamlit as st

BASE_DIRECTORY_PATH = "./screencaps"


def decode_filename(encoded_filename):
    """Decode special characters in directory or file names."""
    return urllib.parse.unquote(encoded_filename)


def display_choices_from_dir(path):
    # ignore hidden files/directories
    encoded_choices = [name for name in os.listdir(path) if not name.startswith(".")]
    decoded_choices = [decode_filename(name) for name in encoded_choices]
    if not encoded_choices:
        st.write(f"`{path}`")
        return path

    # If only option is "default_settings", automatically select it
    if encoded_choices == ["default_settings"]:
        selected_encoded = "default_settings"
    else:
        selected_decoded = st.selectbox(
            "select", decoded_choices, key=path, label_visibility="hidden"
        )
        selected_encoded = encoded_choices[decoded_choices.index(selected_decoded)]

    selected_path = os.path.join(path, selected_encoded)
    if os.path.isdir(selected_path):
        return display_choices_from_dir(selected_path)


def main():
    display_choices_from_dir(BASE_DIRECTORY_PATH)


if __name__ == "__main__":
    main()
