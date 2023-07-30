import json


def get_user_input(prompt, choices):
    for i, choice in enumerate(choices):
        print(f"{i+1}. {choice}")
    selected = int(input(prompt)) - 1
    return choices[selected]


# Load the manifest
with open("manifest.json") as f:
    manifest = json.load(f)

# Get player type
player_type_choices = [player_type for player_type in manifest["players"][0]]
player_type = get_user_input("Select player type: ", player_type_choices)

# Get player brand/model
player_brand_model_choices = [
    f"{player['brand']} {player['model']}"
    for player in manifest["players"][0][player_type]
]
player_brand_model = get_user_input(
    "Select player brand/model: ", player_brand_model_choices
)
player_brand, player_model = player_brand_model.split(maxsplit=1)

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

# Initialize processor chain
processor_chain = []

# Loop for adding processors
while True:
    # Get processor
    processor_choices = [
        f"{processor['brand']} {processor['model']}"
        for processor in manifest["processors"]
        if player_output in processor["inputs"]
    ]
    processor_brand_model = get_user_input("Select processor: ", processor_choices)
    processor_brand, processor_model = processor_brand_model.split(maxsplit=1)

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

# Create folder structure
folder_structure = f"{player_type}/{player_brand}_{player_model}/{player_settings}/{player_output}_{player_output_resolution}"
for i, (
    processor_info,
    processor_settings,
    processor_output,
    processor_output_resolution,
) in enumerate(processor_chain):
    folder_structure += f"/{processor_info}/{processor_settings}/{processor_output}_{processor_output_resolution}"
# Replace spaces with underscores in folder_structure
folder_structure = folder_structure.replace(" ", "_")
print(f"Generated folder structure: {folder_structure}")
