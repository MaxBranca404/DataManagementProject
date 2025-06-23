#!/usr/bin/env python3

# Read the file
with open('charts_processed.csv', 'r') as file:
    lines = file.readlines()

# Process lines: keep first row unchanged, remove .0 from end of other rows
processed_lines = []
for i, line in enumerate(lines):
    if i == 0:  # First row (header) - keep unchanged
        processed_lines.append(line)
    else:  # All other rows - remove .0 from end
        line = line.rstrip('\n\r')  # Remove newline characters
        if line.endswith('.0'):
            line = line[:-2]  # Remove last 2 characters (.0)
        processed_lines.append(line + '\n')

# Write the processed content to output file
with open('final_charts.csv', 'w') as file:
    file.writelines(processed_lines)

print("Processing complete! Output saved to 'final_charts.csv'")
