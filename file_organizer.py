import json
import os
import urllib.parse


def encode_filename(filename):
    """Encode special characters in directory or file names."""
    return urllib.parse.quote(filename, safe="")


def decode_filename(encoded_filename):
    """Decode special characters in directory or file names."""
    return urllib.parse.unquote(encoded_filename)


def get_user_input(prompt, choices):
    for i, choice in enumerate(choices):
        choice = decode_filename(choice) if isinstance(choice, str) else choice
        print(f"{i+1}. {choice}")
    selected = int(input(prompt)) - 1
    return choices[selected]


def organize_files():
    # Load the manifest
    with open("manifest.json") as f:
        manifest = json.load(f)

    # Get player type
    player_type_choices = [player_type for player_type in manifest["players"][0]]
    player_type = get_user_input("Select player type: ", player_type_choices)

    # Create directory for player type
    BASE_DIRECTORY_PATH = (
        os.getcwd()
    )  # Sets the base directory path to the current working directory
    player_type_dir = os.path.join(BASE_DIRECTORY_PATH, player_type)
    os.makedirs(player_type_dir, exist_ok=True)

    # Get player brand/model
    player_brand_model_choices = [
        f"{player['brand']} {player['model']}"
        for player in manifest["players"][0][player_type]
    ]
    player_brand_model = get_user_input(
        "Select player brand/model: ", player_brand_model_choices
    )
    player_brand, player_model = decode_filename(player_brand_model).split(maxsplit=1)

    # Create directory for player brand/model
    player_brand_model_dir = os.path.join(player_type_dir, player_brand_model)
    os.makedirs(player_brand_model_dir, exist_ok=True)

    # Get player settings
    player = next(
        player
        for player in manifest["players"][0][player_type]
        if player["brand"] == player_brand and player["model"] == player_model
    )
    player_settings_dict = {}
    for setting in player["settings"]:
        setting_values_choices = setting["values"]
        chosen_value = get_user_input(
            f"Select value for {setting['name']}: ", setting_values_choices
        )
        player_settings_dict[setting["name"]] = chosen_value

    # Format settings for folder structure
    player_settings = (
        "_".join(f"{k}_{v}" for k, v in player_settings_dict.items())
        if player_settings_dict
        else "default_settings"
    )

    # Create directory for player settings
    player_settings_dir = os.path.join(
        player_brand_model_dir, encode_filename(player_settings)
    )
    os.makedirs(player_settings_dir, exist_ok=True)

    # Get player output and resolution
    player_output_choices = [output["name"] for output in player["outputs"]]
    player_output = get_user_input("Select player output: ", player_output_choices)

    player_output_resolutions = next(
        output["resolutions"]
        for output in player["outputs"]
        if output["name"] == player_output
    )
    # Automatically select resolution if only one is available
    if len(player_output_resolutions) == 1:
        player_output_resolution = player_output_resolutions[0]
    else:
        player_output_resolution = get_user_input(
            "Select output resolution: ", player_output_resolutions
        )

    # Create directory for player output and resolution
    player_output_resolution_dir = os.path.join(
        player_settings_dir,
        encode_filename(f"{player_output}_{player_output_resolution}"),
    )
    os.makedirs(player_output_resolution_dir, exist_ok=True)

    # Initialize processor chain
    processor_chain = []

    # Loop for adding processors
    current_directory = player_output_resolution_dir
    while True:
        # Get processor
        processor_choices = [
            f"{processor['brand']} {processor['model']}"
            for processor in manifest["processors"]
            if player_output in processor["inputs"]
        ]
        processor_brand_model = get_user_input("Select processor: ", processor_choices)
        processor_brand, processor_model = decode_filename(processor_brand_model).split(
            maxsplit=1
        )

        # Create directory for processor brand/model
        processor_brand_model_dir = os.path.join(
            current_directory, processor_brand_model
        )
        os.makedirs(processor_brand_model_dir, exist_ok=True)

        # Get processor settings
        processor = next(
            processor
            for processor in manifest["processors"]
            if processor["brand"] == processor_brand
            and processor["model"] == processor_model
        )
        processor_settings_dict = {}
        for setting in processor["settings"]:
            setting_values_choices = setting["values"]
            chosen_value = get_user_input(
                f"Select value for {setting['name']}: ", setting_values_choices
            )
            processor_settings_dict[setting["name"]] = chosen_value

        # Format settings for folder structure
        processor_settings = (
            "_".join(f"{k}_{v}" for k, v in processor_settings_dict.items())
            if processor_settings_dict
            else "default_settings"
        )

        # Create directory for processor settings
        processor_settings_dir = os.path.join(
            processor_brand_model_dir, encode_filename(processor_settings)
        )
        os.makedirs(processor_settings_dir, exist_ok=True)

        # Get processor output and resolution
        processor_output_choices = [output["name"] for output in processor["outputs"]]
        processor_output = get_user_input(
            "Select processor output: ", processor_output_choices
        )

        processor_output_resolutions = next(
            output["resolutions"]
            for output in processor["outputs"]
            if output["name"] == processor_output
        )
        # Automatically select resolution if only one is available
        if len(processor_output_resolutions) == 1:
            processor_output_resolution = processor_output_resolutions[0]
        else:
            processor_output_resolution = get_user_input(
                "Select output resolution: ", processor_output_resolutions
            )

        # Create directory for processor output and resolution
        processor_output_resolution_dir = os.path.join(
            processor_settings_dir,
            encode_filename(f"{processor_output}_{processor_output_resolution}"),
        )
        os.makedirs(processor_output_resolution_dir, exist_ok=True)

        # Add processor to chain
        processor_chain.append(
            (
                f"{processor_brand}_{processor_model}",
                processor_settings,
                processor_output,
                processor_output_resolution,
            )
        )

        # Update player_output for the next iteration
        player_output = processor_output

        # Ask if another processor should be added
        add_another_processor = get_user_input(
            "Do you want to add another processor? (Yes/No)", ["Yes", "No"]
        )
        if add_another_processor.lower() == "no":
            break

        # Update current_directory for the next processor
        current_directory = processor_output_resolution_dir

    print("Directories created successfully")


def main():
    organize_files()


if __name__ == "__main__":
    main()
