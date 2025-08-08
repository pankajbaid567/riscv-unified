#!/usr/bin/env python3
"""
Simple YAML splitter - converts multi-document YAML to individual files
"""

import yaml
import sys
import os

def split_yaml_file(input_file, output_prefix="inst"):
    """Split a multi-document YAML file into individual files"""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            documents = list(yaml.safe_load_all(f))
        
        output_files = []
        for i, doc in enumerate(documents):
            if doc is None:
                continue
                
            if doc.get('kind') == 'instruction':
                name = doc.get('name', f'unknown_{i}')
                output_file = f"{output_prefix}_{name}.yaml"
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    yaml.safe_dump(doc, f, default_flow_style=False, sort_keys=False)
                
                output_files.append(output_file)
                print(f"Created {output_file}")
        
        return output_files
    
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python split_yaml.py <input_yaml_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        sys.exit(1)
    
    output_files = split_yaml_file(input_file)
    print(f"Split {input_file} into {len(output_files)} files")
