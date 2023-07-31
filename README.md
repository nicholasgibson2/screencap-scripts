# screencap-scripts

## file_organizer.py

This Python script is designed to automate the creation of a directory structure based on user input. The script is particularly useful in organizing files in a hierarchical structure based on various attributes like player type, brand/model, settings, output/resolution, and processors.

### Overview

The file organizer script works by first loading a JSON manifest file that describes the possible choices for each directory level. The script then prompts the user to make choices at each level, which includes:

* Player Type
* Player Brand/Model
* Player Settings
* Player Output/Resolution
* Processor Brand/Model
* Processor Settings
* Processor Output/Resolution

For each choice, a new directory is created. This process is repeated for each processor in the chain. 

The script is designed to handle special characters in directory or file names by URL encoding them. This ensures that all characters can be used in the name, and they can be accurately reverse-engineered losslessly.
