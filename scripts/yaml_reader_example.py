#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YAML file reading example
Demonstrates multiple ways to read YAML files
"""

import yaml
import os
from typing import Dict, Any, List

def read_yaml_basic(file_path: str) -> Dict[str, Any]:
    """
    Basic YAML file reading method
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return {}
    except yaml.YAMLError as e:
        print(f"YAML parse error: {e}")
        return {}

def read_yaml_with_loader(file_path: str) -> Dict[str, Any]:
    """
    Read YAML file with a specific loader
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Use SafeLoader for safety
            data = yaml.load(file, Loader=yaml.SafeLoader)
        return data
    except Exception as e:
        print(f"Read error: {e}")
        return {}

def read_yaml_all_documents(file_path: str) -> List[Dict[str, Any]]:
    """
    Read YAML file containing multiple documents
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            documents = list(yaml.safe_load_all(file))
        return documents
    except Exception as e:
        print(f"Read error: {e}")
        return []

def write_yaml_example():
    """
    Example of writing a YAML file
    """
    data = {
        'names': ['b_fully_ripened', 'b_half_ripened', 'b_green'],
        'nc': 3,
        'path': './dataset',
        'train': 'train/images',
        'val': 'val/images'
    }
    
    try:
        with open('output_example.yaml', 'w', encoding='utf-8') as file:
            yaml.dump(data, file, default_flow_style=False, allow_unicode=True)
        print("YAML file written successfully: output_example.yaml")
    except Exception as e:
        print(f"Write error: {e}")

def main():
    """Main function, demonstrates various YAML reading methods"""
    
    # Script is in scripts/, so go up one level to get dataset root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Read existing YAML file (from data/origin/)
    yaml_file = os.path.join(base_dir, "data", "origin", "example_dataset.yaml")
    
    print("=== Method 1: Basic Reading ===")
    data1 = read_yaml_basic(yaml_file)
    print(f"Data read: {data1}")
    
    print("\n=== Method 2: Using SafeLoader ===")
    data2 = read_yaml_with_loader(yaml_file)
    print(f"Data read: {data2}")
    
    print("\n=== Access Specific Fields ===")
    if data1:
        print(f"Class names: {data1.get('names', [])}")
        print(f"Number of classes: {data1.get('nc', 0)}")
        print(f"Dataset path: {data1.get('path', '')}")
        print(f"Train path: {data1.get('train', '')}")
        print(f"Validation path: {data1.get('val', '')}")
    
    print("\n=== Method 3: Read Multi-document YAML ===")
    # Create multi-document YAML example
    multi_doc_content = """
---
document1:
  name: "First document"
  value: 100
---
document2:
  name: "Second document"
  value: 200
"""
    
    with open('multi_doc_example.yaml', 'w', encoding='utf-8') as f:
        f.write(multi_doc_content)
    
    documents = read_yaml_all_documents('multi_doc_example.yaml')
    print(f"Multi-document YAML: {documents}")
    
    print("\n=== YAML File Write Example ===")
    write_yaml_example()
    
    # Clean up temporary file
    if os.path.exists('multi_doc_example.yaml'):
        os.remove('multi_doc_example.yaml')

if __name__ == "__main__":
    main() 