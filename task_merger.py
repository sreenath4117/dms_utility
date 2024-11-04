import json
import os

def merge_json_files(input_folder, output_folder, output_filename):
    # Ensure output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Initialize a list to hold all rules
    merged_rules = []

    # Iterate through all files in the input directory
    for filename in sorted(os.listdir(input_folder)):  # Sort to maintain order
        if filename.endswith('.json'):  # Check for JSON files
            file_path = os.path.join(input_folder, filename)
            with open(file_path, 'r') as json_file:
                try:
                    # Load the JSON data from the file
                    data = json.load(json_file)
                    # Append the rules from this file to the merged_rules list
                    if 'rules' in data:
                        merged_rules.extend(data['rules'])  # Add all rules under one root
                except json.JSONDecodeError as e:
                    print(f"Error reading {filename}: {e}")

    # Write the merged rules to a new JSON file under a single root
    output_file_path = os.path.join(output_folder, output_filename)
    merged_data = {"rules": merged_rules}  # Create a single root for all rules
    
    with open(output_file_path, 'w') as output_file:
        json.dump(merged_data, output_file, indent=4)

    print(f"Merged JSON files into {output_file_path}")

# Example usage
merge_json_files(
    input_folder='output/created_task',  # Folder containing the individual JSON files
    output_folder='output/unsort_output',        # Folder to save the merged JSON file
    output_filename='merged_output.json'   # Name of the merged output file
)
