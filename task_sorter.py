import json
import os

def renumber_dms_rules(rules):
    # Renumber rule-id and rule-name while maintaining original order
    for index, rule in enumerate(rules):
        rule['rule-id'] = index + 1
        rule['rule-name'] = index + 1

    return rules

def process_files_in_folder(input_folder, output_file_path):
    all_rules = []

    for filename in os.listdir(input_folder):
        if filename.endswith('.json'):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
                # Extend with rules from this file while keeping original order
                if 'rules' in data:
                    all_rules.extend(data['rules'])

    # Renumber the combined rules
    sorted_rules = renumber_dms_rules(all_rules)

    output_data = {'rules': sorted_rules}

    # Write the combined sorted data to a single output file
    with open(output_file_path, 'w') as output_file:
        json.dump(output_data, output_file, indent=4)

    print(f"Combined sorted rules have been written to {output_file_path}")

if __name__ == "__main__":
    input_folder = 'output/unsort_output'  
    output_file_path = 'output/sort_output/sorted_output.json'
    
    # Create output folder if it doesn't exist
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    
    process_files_in_folder(input_folder, output_file_path)
