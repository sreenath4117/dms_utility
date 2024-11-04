# AWS DMS Task JSON Generator, Sorter, and Merger

## Overview

The AWS DMS Task JSON Generator, Sorter, and Merger is a Python project designed to generate and manage AWS Database Migration Service (DMS) task JSON files. The project consists of three main functionalities:

- **Generating DMS Task JSON Files**: Create AWS DMS task JSON files based on transformation rules specified in CSV files.
- **Merging DMS Task JSON Files**: Combine multiple DMS task JSON files into a single file while maintaining the order of rules.
- **Sorting and Renumbering DMS Rules**: Sort the combined rules by their IDs and renumber them sequentially.

## Features

### DMS Task JSON Generation:

- Reads column transformation rules from a CSV file.
- Generates JSON rules for AWS DMS tasks, including:
  - Table selection
  - Table renaming
  - Column renaming
  - Column removal
- Supports dynamic output file naming based on the table name.
- Overwrites existing output files to keep the latest configuration.

### DMS Task Merging:

- Merges multiple JSON files containing DMS rules.
- Maintains the order of rules from each source file.
- Outputs a single consolidated JSON file for easier management.

### DMS Rules Sorting:

- Sorts the merged rules by `rule-id`.
- Renumbers the rules sequentially for consistency.

## Requirements

- Python 3.x
- Pandas library

## Installation

To install the required library, run:

```bash
pip install pandas

```

## Usage

### 1. Generating DMS Task JSON Files

**Prepare Your Reference CSV File:**  
Create a CSV file named after your table (e.g., `table_name.csv`) and place it in a folder named `reference`.  
The CSV should have two columns:

- **`columnA`**: Current column names.
- **`columnB`**: New column names (leave empty if you want to remove the column).

**Example `table_name.csv`:**

```csv
columnA,columnB
fv_id,Vitals_Id
fv_groupname,
fv_date,Date_Of_Vitals
fv_value,Value_Of_Vitals
```

### 2. Run the Script:

Update the script parameters in the function call at the bottom of the script:

```python

generate_dms_task_json(
reference_folder='reference', # Folder where reference files are located
database_name='database_name',
old_table_name='table_name', # Name of the table (and corresponding CSV file)
new_table_name='table_new_name' # New Name of the table at target
)

```

**Execute the script:**

```bash

    python task_maker.py

```

### 3. Output:

The generated JSON file will be saved in the output/created_task/ directory with a name based on the table name (e.g., zhemr_form_vitals_dms_task.json).
If a file with that name already exists, it will be overwritten.

## Merging DMS Task JSON Files

### 1. Prepare Your Input Folder:

Ensure that all your generated JSON files from output/created_task are ready for merging. The `task_merger.py` script will read from this folder.

### 2. Run the Merging Script:

Update the parameters in the script as needed:

```python
input_folder = 'output/created_task'  # Folder containing individual JSON files
output_folder = 'output/unsort_output' # Folder to save merged output file
output_filename = 'merged_output.json'  # Name of merged output file
```

**Execute the merging script:**

```bash
python task_merger.py
```

### 3. Output:

The merged rules will be written to output/unsort_output/merged_output.json, combining all input files under one root while preserving their order.

## Sorting and Renumbering DMS Rules

### 1. Prepare Your Input Folder:

The `task_sorter.py` script will read directly from the output/unsort_output folder, where the merged JSON file is saved by `task_merger.py`.

### 2. Run the Sorting Script:

Update the parameters in the script as needed:

```python

input_folder = 'output/unsort_output'
output_file_path = 'output/sort_output/sorted_output.json'

```

**Execute the sorting script:**

```bash

python task_sorter.py

```

### 3. Output:

The combined and sorted rules will be written to output/sort_output/sorted_output.json.

### Contributing

If you wish to contribute to this project, please fork the repository and submit a pull request with your changes.

### License

This project is licensed under the MIT License. See the LICENSE file for more details. This README file includes formatted code blocks using triple backticks (```) to highlight installation commands, example CSV content, and Python code snippets effectively. You can copy this content directly into a README.md file in your project repository. If you need further modifications or additional sections, feel free to ask!
