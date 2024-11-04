import json
import pandas as pd
import os

def generate_dms_task_json(reference_folder, database_name, old_table_name, new_table_name):
    # Construct the path to the reference file based on the table name
    reference_file = os.path.join(reference_folder, f"{old_table_name}.csv")

    # Load the reference file into a DataFrame
    df = pd.read_csv(reference_file)

    # Prepare new rules list
    new_rules = []

    # Add a selection rule for the table
    table_selection_rule = {
        "rule-type": "selection",
        "rule-id": 1,
        "rule-name": 1,
        "object-locator": {
            "schema-name": database_name,
            "table-name": old_table_name
        },
        "rule-action": "include",
        "filters": []
    }
    new_rules.append(table_selection_rule)

    # Add a transformation rule for renaming the table
    table_rename_rule = {
        "rule-type": "transformation",
        "rule-id": 2,
        "rule-name": 2,
        "rule-target": "table",
        "object-locator": {
            "schema-name": database_name,
            "table-name": old_table_name
        },
        "rule-action": "rename",
        "value": new_table_name,
        "old-value": None
    }
    new_rules.append(table_rename_rule)

    # Create a list to hold column rename rules
    column_rename_rules = []
    
    # Iterate through the DataFrame rows for column transformations
    for index, row in df.iterrows():
        column_name = row['columnA']
        new_column_name = row['columnB']

        rule_id = index + 3

        if pd.notna(new_column_name) and new_column_name:
            rule = {
                "rule-type": "transformation",
                "rule-id": rule_id,
                "rule-name": rule_id,
                "rule-target": "column",
                "object-locator": {
                    "schema-name": database_name,
                    "table-name": old_table_name,
                    "column-name": column_name
                },
                "rule-action": "rename",
                "value": new_column_name,
                "old-value": None
            }
            column_rename_rules.append(rule)

    # Add all column rename rules first
    new_rules.extend(column_rename_rules)

    # Now add remove-column rules for any columns that need to be removed
    for index, row in df.iterrows():
        column_name = row['columnA']
        new_column_name = row['columnB']

        if pd.isna(new_column_name) or new_column_name == '':
            rule_id = index + 3 + len(column_rename_rules)
            
            rule = {
                "rule-type": "transformation",
                "rule-id": rule_id,
                "rule-name": rule_id,
                "rule-target": "column",
                "object-locator": {
                    "schema-name": database_name,
                    "table-name": old_table_name,
                    "column-name": column_name
                },
                "rule-action": "remove-column", 
                "value": None,
                "old-value": None
            }
            new_rules.append(rule)

    # Ensure output directory exists
    output_directory = 'output/created_task/'
    os.makedirs(output_directory, exist_ok=True)

    # Determine output file path based on table name (overwrite if exists)
    output_file_path = os.path.join(output_directory, f"{old_table_name}_dms_task.json")

    # Write the JSON data to the determined file path (overwrites if exists)
    dms_task_json = {"rules": new_rules}
    
    with open(output_file_path, 'w') as json_file:  # Open in write mode to overwrite if exists
        json.dump(dms_task_json, json_file, indent=4)

# Example usage with placeholders
generate_dms_task_json(
    reference_folder='reference',  # Folder where reference files are located
    database_name='metrolivezh',
    old_table_name='zhemr_inv_branches',  # Name of the table (and corresponding CSV file)
    new_table_name='model_inventory_branches'
)
