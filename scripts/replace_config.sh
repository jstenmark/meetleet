#!/bin/bash
# replace_config.sh

# Define the directory to search
search_dir="src"

# Old and new ways of accessing config values
old_pattern="config\."
new_pattern="config.config_data.get("

# Loop through Python files in the directory
for file in $(find $search_dir -name "*.py"); do
  echo "Processing $file"

  # Use sed to replace the old pattern with the new one
  sed -i "s/$old_pattern\([A-Za-z_0-9]*\)\([^A-Za-z_0-9]\)/$new_pattern\'\1\', {})\.get(\'\1\', None)\2/g" "$file"

  echo "Replaced old pattern in $file"
done

echo "Replacement completed."
