#!/usr/bin/env python3
"""Convert tomato ripeness detection annotations to COCO JSON.

This script converts per-image CSV annotations into COCO-style JSON files.

Usage examples:
    python scripts/convert_to_coco.py --root . --out annotations --splits train val test
"""

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Sequence

from PIL import Image


def _read_split_list(split_file: Path) -> List[str]:
    """Read image base names (without extension) from a split file."""
    if not split_file.exists():
        return []
    lines = [line.strip() for line in split_file.read_text(encoding="utf-8").splitlines()]
    return [line for line in lines if line]


def _image_size(image_path: Path) -> tuple[int, int]:
    """Return (width, height) for an image path using PIL."""
    with Image.open(image_path) as img:
        return img.width, img.height


def _parse_csv_boxes(csv_path: Path) -> List[Dict[str, float]]:
    """Parse a single per-image CSV file and return COCO-style bboxes."""
    if not csv_path.exists():
        return []
    
    boxes: List[Dict[str, float]] = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            return boxes
        
        # Normalize header keys to lowercase
        header_lower = {k.lower(): k for k in reader.fieldnames}
        
        for row in reader:
            # Get values with case-insensitive lookup
            def get_value(*keys: str) -> Optional[float]:
                for key in keys:
                    key_lower = key.lower()
                    if key_lower in header_lower:
                        orig_key = header_lower[key_lower]
                        if orig_key in row and row[orig_key]:
                            try:
                                return float(row[orig_key])
                            except ValueError:
                                continue
                return None
            
            x = get_value("x", "xc", "x_center")
            y = get_value("y", "yc", "y_center")
            w = get_value("w", "width", "dx")
            h = get_value("h", "height", "dy")
            label = get_value("label", "class", "category_id")
            
            if x is not None and y is not None and w is not None and h is not None:
                boxes.append({
                    "x": x,
                    "y": y,
                    "width": w,
                    "height": h,
                    "label": int(label) if label is not None else 1
                })
    
    return boxes


def _load_labelmap(labelmap_path: Path) -> Dict[int, str]:
    """Load labelmap.json and return a mapping from label_id to object_name."""
    if not labelmap_path.exists():
        return {}
    
    with open(labelmap_path, 'r', encoding='utf-8') as f:
        labelmap = json.load(f)
    
    mapping = {}
    for item in labelmap:
        label_id = item.get("label_id", item.get("object_id"))
        object_name = item.get("object_name", "")
        mapping[label_id] = object_name
    
    return mapping


def _collect_annotations_for_split(
    category_root: Path,
    split: str,
    labelmap: Dict[int, str],
) -> tuple[List[Dict], List[Dict], List[Dict]]:
    """Collect COCO dictionaries for images, annotations, and categories."""
    images_dir = category_root / "images"
    annotations_dir = category_root / "csv"
    sets_dir = category_root / "sets"
    
    split_file = sets_dir / f"{split}.txt"
    image_stems = set(_read_split_list(split_file))
    if not image_stems:
        # If no split list is provided, fall back to all images
        image_stems = {p.stem for p in images_dir.glob("*.jpg")}
        image_stems.update({p.stem for p in images_dir.glob("*.png")})
        image_stems.update({p.stem for p in images_dir.glob("*.bmp")})
    
    images: List[Dict] = []
    anns: List[Dict] = []
    
    # Build categories from labelmap (skip background if present)
    categories: List[Dict] = []
    for label_id, name in sorted(labelmap.items()):
        if label_id == 0 and name.lower() == "background":
            continue
        categories.append({
            "id": label_id,
            "name": name,
            "supercategory": "tomato_ripeness"
        })
    
    image_id_counter = 1
    ann_id_counter = 1
    
    for stem in sorted(image_stems):
        # Try different image formats
        img_path = None
        for ext in [".jpg", ".jpeg", ".png", ".bmp"]:
            candidate = images_dir / f"{stem}{ext}"
            if candidate.exists():
                img_path = candidate
                break
        
        if img_path is None:
            continue
        
        width, height = _image_size(img_path)
        images.append({
            "id": image_id_counter,
            "file_name": str(img_path.relative_to(category_root.parent)),
            "width": width,
            "height": height,
        })
        
        csv_path = annotations_dir / f"{stem}.csv"
        for box in _parse_csv_boxes(csv_path):
            category_id = box.get("label", 1)
            # Skip background category
            if category_id == 0:
                continue
            
            anns.append({
                "id": ann_id_counter,
                "image_id": image_id_counter,
                "category_id": category_id,
                "bbox": [box["x"], box["y"], box["width"], box["height"]],
                "area": box["width"] * box["height"],
                "iscrowd": 0,
            })
            ann_id_counter += 1
        
        image_id_counter += 1
    
    return images, anns, categories


def _build_coco_dict(
    images: List[Dict],
    anns: List[Dict],
    categories: List[Dict],
    description: str,
) -> Dict:
    """Build a complete COCO dict from components."""
    return {
        "info": {
            "year": 2020,
            "version": "2.0",
            "description": description,
            "url": "https://laboro.ai/",
            "contributor": "Laboro.ai",
        },
        "images": images,
        "annotations": anns,
        "categories": categories,
        "licenses": [
            {
                "id": 1,
                "name": "Attribution-NonCommercial-ShareAlike License",
                "url": "http://creativecommons.org/licenses/by-nc-sa/4.0/"
            }
        ],
    }


def convert(
    root: Path,
    out_dir: Path,
    category: str,
    splits: Sequence[str],
) -> None:
    """Convert selected category and splits to COCO JSON files."""
    out_dir.mkdir(parents=True, exist_ok=True)
    
    category_root = root / category
    labelmap_path = category_root / "labelmap.json"
    labelmap = _load_labelmap(labelmap_path)
    
    for split in splits:
        images, anns, categories = _collect_annotations_for_split(
            category_root, split, labelmap
        )
        desc = f"Tomato Ripeness Detection {category} {split} split"
        coco = _build_coco_dict(images, anns, categories, desc)
        out_path = out_dir / f"{category}_instances_{split}.json"
        out_path.write_text(json.dumps(coco, indent=2), encoding="utf-8")
        print(f"Generated: {out_path} ({len(images)} images, {len(anns)} annotations)")


def main() -> int:
    """Entry point for the converter CLI."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Dataset root containing category subfolders (default: dataset root)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "annotations",
        help="Output directory for COCO JSON files (default: <root>/annotations)",
    )
    parser.add_argument(
        "--category",
        type=str,
        default="tomatoes",
        help="Category to convert (default: tomatoes)",
    )
    parser.add_argument(
        "--splits",
        nargs="+",
        type=str,
        default=["train", "val", "test"],
        choices=["train", "val", "test"],
        help="Dataset splits to generate (default: train val test)",
    )
    
    args = parser.parse_args()
    
    convert(
        root=Path(args.root),
        out_dir=Path(args.out),
        category=args.category,
        splits=args.splits,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())





