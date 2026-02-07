#python src\test_b_json_load.py

import json

# Open the JSON file
with open('src/json/demo_npc.json', 'r') as f:
    cl_data = json.load(f)  # Load JSON content into a Python object

# Print the data
print(cl_data)
