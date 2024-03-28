import json

# Specify the path to your JSON file
json_file_path = '/home/ubuntu/app/indexing/preprocessed_new_input.json'

# Specify the path to the output file
output_file_path = 'text.txt'

# Open and read the JSON file with utf-8 encoding
with open(json_file_path, 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# Open the output file for writing, also with utf-8 encoding
with open(output_file_path, 'w', encoding='utf-8') as file:
    # Iterate through the JSON data
    for key, value in json_data.items():
        # Write each value to the file, followed by two newline characters for separation
        file.write(value + '\n\n')

print(f"Data has been written to {output_file_path}")