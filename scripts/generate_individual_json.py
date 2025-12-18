#!/usr/bin/env python3
import json
import os
import random
import time
from PIL import Image

def generate_unique_id():
    random_part = random.randint(1000000, 9999999)
    timestamp_part = int(time.time()) % 1000
    return int(f"{random_part}{timestamp_part:03d}")

def get_image_info(image_path):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            file_size = os.path.getsize(image_path)
            return {"width": width, "height": height, "size": file_size, "format": img.format or "JPEG"}
    except Exception as e:
        print(f"Error reading image {image_path}: {e}")
        return {"width": 512, "height": 512, "size": 0, "format": "JPEG"}

def get_category_name(category_id):
    categories = {0: "b_fully_ripened", 1: "b_half_ripened", 2: "b_green", 3: "l_fully_ripened", 4: "l_half_ripened", 5: "l_green"}
    return categories.get(category_id, f"category_{category_id}")

def create_individual_json(image_path, image_annotations, base_annotations_file):
    image_id = generate_unique_id()
    annotation_ids = [generate_unique_id() for _ in range(len(image_annotations))]
    
    image_info = get_image_info(image_path)
    file_name = os.path.basename(image_path)
    
    image_entry = {
        "id": image_id,
        "width": image_info["width"],
        "height": image_info["height"],
        "file_name": file_name,
        "size": image_info["size"],
        "format": image_info["format"],
        "url": "",
        "hash": "",
        "status": "success"
    }
    
    annotation_entries = []
    for i, ann in enumerate(image_annotations):
        annotation_entry = {
            "id": annotation_ids[i],
            "image_id": image_id,
            "category_id": ann.get("category_id", 0),
            "segmentation": ann.get("segmentation", []),
            "area": ann.get("area", 0),
            "bbox": ann.get("bbox", [0, 0, 100, 100])
        }
        annotation_entries.append(annotation_entry)
    
    category_ids = set(ann.get("category_id", 0) for ann in image_annotations)
    categories = []
    for cat_id in category_ids:
        categories.append({
            "id": cat_id,
            "name": get_category_name(cat_id),
            "supercategory": "Tomato Ripeness"
        })
    
    json_data = {
        "info": {
            "description": "Individual image annotation",
            "version": "1.0",
            "year": 2025,
            "contributor": "search engine",
            "source": "augmented",
            "license": {
                "name": "Creative Commons Attribution 4.0 International",
                "url": "https://creativecommons.org/licenses/by/4.0/"
            }
        },
        "images": [image_entry],
        "annotations": annotation_entries,
        "categories": categories
    }
    
    return json_data

def load_annotations(annotations_file):
    try:
        with open(annotations_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        annotations_by_file = {}
        for ann in data.get("annotations", []):
            image_id = ann.get("image_id")
            for img in data.get("images", []):
                if img.get("id") == image_id:
                    filename = img.get("file_name")
                    if filename not in annotations_by_file:
                        annotations_by_file[filename] = []
                    annotations_by_file[filename].append(ann)
                    break
        
        return annotations_by_file
    except Exception as e:
        print(f"Error loading annotations from {annotations_file}: {e}")
        return {}

def process_images_folder(images_folder, labels_folder, annotations_file, output_folder):
    annotations_by_file = load_annotations(annotations_file)
    
    for image_file in os.listdir(images_folder):
        if image_file.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(images_folder, image_file)
            
            image_annotations = annotations_by_file.get(image_file, [])
            
            if not image_annotations:
                label_file = os.path.join(labels_folder, os.path.splitext(image_file)[0] + '.txt')
                if os.path.exists(label_file):
                    image_annotations = create_annotations_from_label(label_file)
            
            json_data = create_individual_json(image_path, image_annotations, annotations_file)
            
            json_filename = os.path.splitext(image_file)[0] + '.json'
            json_path = os.path.join(images_folder, json_filename)
            
            try:
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, indent=2, ensure_ascii=False)
                print(f"Generated: {json_path}")
            except Exception as e:
                print(f"Error saving {json_path}: {e}")

def create_annotations_from_label(label_file):
    annotations = []
    try:
        with open(label_file, 'r') as f:
            lines = f.readlines()
        
        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 5:
                category_id = int(parts[0])
                center_x = float(parts[1])
                center_y = float(parts[2])
                width = float(parts[3])
                height = float(parts[4])
                
                bbox_x = center_x - width/2
                bbox_y = center_y - height/2
                bbox_w = width
                bbox_h = height
                
                annotation = {
                    "category_id": category_id,
                    "bbox": [bbox_x, bbox_y, bbox_w, bbox_h],
                    "area": bbox_w * bbox_h,
                    "segmentation": []
                }
                annotations.append(annotation)
    except Exception as e:
        print(f"Error reading label file {label_file}: {e}")
    
    return annotations

def main():
    # Script is in scripts/, so go up one level to get dataset root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    print("Processing train folder...")
    train_images = os.path.join(base_dir, "data", "origin", "train", "images")
    train_labels = os.path.join(base_dir, "data", "origin", "train", "labels")
    train_annotations = os.path.join(base_dir, "annotations", "train.json")
    
    if os.path.exists(train_images):
        process_images_folder(train_images, train_labels, train_annotations, train_images)
    
    print("\nProcessing val folder...")
    val_images = os.path.join(base_dir, "data", "origin", "val", "images")
    val_labels = os.path.join(base_dir, "data", "origin", "val", "labels")
    val_annotations = os.path.join(base_dir, "annotations", "test.json")
    
    if os.path.exists(val_images):
        process_images_folder(val_images, val_labels, val_annotations, val_images)
    
    print("\nIndividual JSON generation completed!")

if __name__ == "__main__":
    main() 