#!/bin/bash
# File: scripts/cleanup.sh
# Purpose: Script to clean up temporary files in a Python project.

# Remove .tmp files
find . -type f -name '*.tmp' -exec rm -f {} +

# Remove .bak files
find . -type f -name '*.bak' -exec rm -f {} +

# Remove .swp files
find . -type f -name '*.swp' -exec rm -f {} +

# Clean up tmp
rm -f ./tmp/*
