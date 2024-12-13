#!/bin/bash

rm -rf tests/*-relabeled*
# Iterate through all .bril files in the tests directory
for file in tests/*.bril; do
    # Extract just the filename without extension and directory
    filename=$(basename "$file" .bril)
    
    # Run the relabeling step
    python relabel.py "tests/${filename}.bril" > "tests/${filename}-relabeled.bril"
    
    # Convert to JSON
    bril2json < "tests/${filename}-relabeled.bril" > "tests/${filename}-relabeled.json"
    
    # Run CFG analysis and capture its exit status
    if ! python cfg.py "tests/${filename}-relabeled.json"; then
        echo "Error: CFG analysis failed for ${filename}"
        exit 1
    fi
    
    echo "Successfully processed ${filename}"
done
