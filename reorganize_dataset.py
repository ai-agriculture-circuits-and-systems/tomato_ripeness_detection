#!/usr/bin/env python3
"""
Reorganize tomato ripeness detection dataset to standard structure.
Converts YOLO format to CSV format and reorganizes directory structure.
"""
import os
import shutil
import csv
from pathlib import Path
from PIL import Image

# Category mapping (YOLO uses 0-indexed, but we'll use 1-indexed for labelmap)
CATEGORY_NAMES = {
    0: "b_fully_ripened",
    1: "b_half_ripened", 
    2: "b_green",
    3: "l_fully_ripened",
    4: "l_half_ripened",
    5: "l_green"
}

def yolo_to_bbox(yolo_line, img_width, img_height):
    """Convert YOLO format (normalized center_x, center_y, width, height) to pixel bbox (x, y, width, height)."""
    parts = yolo_line.strip().split()
    if len(parts) < 5:
        return None
    
    category_id = int(parts[0])
    center_x_norm = float(parts[1])
    center_y_norm = float(parts[2])
    width_norm = float(parts[3])
    height_norm = float(parts[4])
    
    # Convert normalized coordinates to pixel coordinates
    center_x = center_x_norm * img_width
    center_y = center_y_norm * img_height
    width = width_norm * img_width
    height = height_norm * img_height
    
    # Convert center to top-left corner
    x = center_x - width / 2
    y = center_y - height / 2
    
    return {
        'category_id': category_id + 1,  # Convert to 1-indexed for labelmap
        'x': x,
        'y': y,
        'width': width,
        'height': height
    }

def convert_yolo_to_csv(yolo_file, csv_file, img_path):
    """Convert YOLO format label file to CSV format."""
    # Get image dimensions
    try:
        with Image.open(img_path) as img:
            img_width, img_height = img.size
    except Exception as e:
        print(f"Warning: Could not read image {img_path}: {e}")
        return False
    
    # Read YOLO labels
    annotations = []
    try:
        with open(yolo_file, 'r') as f:
            for line in f:
                bbox = yolo_to_bbox(line, img_width, img_height)
                if bbox:
                    annotations.append(bbox)
    except Exception as e:
        print(f"Error reading YOLO file {yolo_file}: {e}")
        return False
    
    # Write CSV file
    try:
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['#item', 'x', 'y', 'width', 'height', 'label'])
            for i, ann in enumerate(annotations):
                writer.writerow([
                    i,
                    round(ann['x'], 2),
                    round(ann['y'], 2),
                    round(ann['width'], 2),
                    round(ann['height'], 2),
                    ann['category_id']
                ])
        return True
    except Exception as e:
        print(f"Error writing CSV file {csv_file}: {e}")
        return False

def get_image_stem(image_path):
    """Get image filename without extension."""
    return Path(image_path).stem

def reorganize_dataset():
    """Main function to reorganize the dataset."""
    base_dir = Path(__file__).parent
    tomatoes_dir = base_dir / "tomatoes"
    images_dir = tomatoes_dir / "images"
    csv_dir = tomatoes_dir / "csv"
    
    # Create directories
    images_dir.mkdir(parents=True, exist_ok=True)
    csv_dir.mkdir(parents=True, exist_ok=True)
    
    # Process train and val splits
    train_images = []
    val_images = []
    
    # Process train split
    train_img_dir = base_dir / "train" / "images"
    train_label_dir = base_dir / "train" / "labels"
    
    if train_img_dir.exists():
        print("Processing train split...")
        for img_file in train_img_dir.glob("*.jpg"):
            img_stem = get_image_stem(img_file)
            label_file = train_label_dir / f"{img_stem}.txt"
            
            # Copy image
            dest_img = images_dir / img_file.name
            shutil.copy2(img_file, dest_img)
            train_images.append(img_stem)
            
            # Convert label to CSV
            if label_file.exists():
                csv_file = csv_dir / f"{img_stem}.csv"
                convert_yolo_to_csv(label_file, csv_file, img_file)
            else:
                print(f"Warning: No label file found for {img_file}")
    
    # Process val split
    val_img_dir = base_dir / "val" / "images"
    val_label_dir = base_dir / "val" / "labels"
    
    if val_img_dir.exists():
        print("Processing val split...")
        for img_file in val_img_dir.glob("*.jpg"):
            img_stem = get_image_stem(img_file)
            label_file = val_label_dir / f"{img_stem}.txt"
            
            # Copy image
            dest_img = images_dir / img_file.name
            shutil.copy2(img_file, dest_img)
            val_images.append(img_stem)
            
            # Convert label to CSV
            if label_file.exists():
                csv_file = csv_dir / f"{img_stem}.csv"
                convert_yolo_to_csv(label_file, csv_file, img_file)
            else:
                print(f"Warning: No label file found for {img_file}")
    
    # Create sets files
    sets_dir = tomatoes_dir / "sets"
    sets_dir.mkdir(parents=True, exist_ok=True)
    
    # Write train.txt
    with open(sets_dir / "train.txt", 'w') as f:
        for img_stem in sorted(train_images):
            f.write(f"{img_stem}\n")
    
    # Write val.txt
    with open(sets_dir / "val.txt", 'w') as f:
        for img_stem in sorted(val_images):
            f.write(f"{img_stem}\n")
    
    # Write all.txt
    all_images = sorted(train_images + val_images)
    with open(sets_dir / "all.txt", 'w') as f:
        for img_stem in all_images:
            f.write(f"{img_stem}\n")
    
    # Write train_val.txt
    with open(sets_dir / "train_val.txt", 'w') as f:
        for img_stem in sorted(train_images + val_images):
            f.write(f"{img_stem}\n")
    
    # For test.txt, we'll use val as test (since original dataset doesn't have separate test)
    with open(sets_dir / "test.txt", 'w') as f:
        for img_stem in sorted(val_images):
            f.write(f"{img_stem}\n")
    
    print(f"\nReorganization complete!")
    print(f"  Train images: {len(train_images)}")
    print(f"  Val images: {len(val_images)}")
    print(f"  Total images: {len(all_images)}")

if __name__ == "__main__":
    reorganize_dataset()





