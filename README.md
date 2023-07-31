# Screencap Directory Organizer and Browser

This project contains two Python scripts: `file_organizer.py` and `browser.py`, and a configuration file `manifest.json`.

## file_organizer.py

This script automates the creation of a directory structure based on user input. The user is prompted to make choices at each level for various attributes such as player type, brand/model, settings, output/resolution, and processors. 

## manifest.json

This is a configuration file that defines the possible choices for each directory level, including the player types, brands/models, outputs, settings, and processors. The `file_organizer.py` script uses this file as a guide to prompt the user for input. 

## browser.py

This script is a Streamlit application that allows the user to navigate the directory structure created by `file_organizer.py` through a web interface. The script reads the directory structure and presents the extracted information to the user as choices in selectboxes. The user can then select an option from the dropdown list.

If a directory contains only the 'default_settings' folder, the script automatically selects it and moves to the next level. If a directory or file name contains URL-encoded characters, the script decodes them for display. The original URL-encoded names are preserved in the underlying file system.

To run the Streamlit application, save the script into a Python file (for example, `browser.py`), and then run the command `streamlit run browser.py` in the terminal.

Please note that you need to have Streamlit installed to run this application. If you don't have it installed, you can install it using pip: `pip install streamlit`.

