#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple YAML file reading example
Specifically for tomato ripeness dataset
"""

import yaml

def read_dataset_config(yaml_file_path: str):
    """
    Read dataset config file
    """
    try:
        with open(yaml_file_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        
        print("=== Dataset Config Info ===")
        print(f"Class names: {config['names']}")
        print(f"Number of classes: {config['nc']}")
        print(f"Dataset path: {config['path']}")
        print(f"Train path: {config['train']}")
        print(f"Validation path: {config['val']}")
        
        return config
        
    except FileNotFoundError:
        print(f"Error: File not found {yaml_file_path}")
        return None
    except yaml.YAMLError as e:
        print(f"Error: YAML format error - {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def access_specific_data(config):
    """
    Access specific config data
    """
    if config is None:
        return
    
    print("\n=== Data Access Example ===")
    
    # Get all class names
    class_names = config.get('names', [])
    print(f"All classes: {class_names}")
    
    # Get the first class
    if class_names:
        print(f"First class: {class_names[0]}")
    
    # Get number of classes
    num_classes = config.get('nc', 0)
    print(f"Total number of classes: {num_classes}")
    
    # Build full paths
    base_path = config.get('path', '')
    train_path = config.get('train', '')
    val_path = config.get('val', '')
    
    full_train_path = f"{base_path}/{train_path}" if base_path and train_path else train_path
    full_val_path = f"{base_path}/{val_path}" if base_path and val_path else val_path
    
    print(f"Full train path: {full_train_path}")
    print(f"Full validation path: {full_val_path}")

def main():
    """
    Main function
    """
    # Script is in scripts/, so go up one level to get dataset root
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Read your dataset config file (from data/origin/)
    yaml_file = os.path.join(base_dir, "data", "origin", "example_dataset.yaml")
    
    print("Reading YAML config file...")
    config = read_dataset_config(yaml_file)
    
    if config:
        access_specific_data(config)
        
        print("\n=== Full config dict ===")
        print(config)

if __name__ == "__main__":
    main() 