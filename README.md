# Tomato Ripeness Detection Dataset

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/your-repo/tomato-ripeness-detection)

A comprehensive dataset of tomato images for ripeness detection and classification, collected and organized for computer vision and deep learning research in agricultural applications.

**Project page**: `https://www.kaggle.com/datasets/nexuswho/laboro-tomato`

## TL;DR

- **Task**: Object Detection, Classification
- **Modality**: RGB
- **Platform**: Ground/Field
- **Real/Synthetic**: Real
- **Images**: 804 tomato images across 6 ripeness/health categories (b_fully_ripened, b_half_ripened, b_green, l_fully_ripened, l_half_ripened, l_green)
- **Resolution**: Variable (typically 3024×4032 or 3120×4160 pixels)
- **Annotations**: CSV (per-image), COCO JSON (generated)
- **License**: CC BY-NC-SA 4.0
- **Citation**: see below

## Table of Contents

- [Download](#download)
- [Dataset Structure](#dataset-structure)
- [Sample Images](#sample-images)
- [Annotation Schema](#annotation-schema)
- [Stats and Splits](#stats-and-splits)
- [Quick Start](#quick-start)
- [Evaluation and Baselines](#evaluation-and-baselines)
- [Datasheet (Data Card)](#datasheet-data-card)
- [Known Issues and Caveats](#known-issues-and-caveats)
- [License](#license)
- [Citation](#citation)
- [Changelog](#changelog)
- [Contact](#contact)

## Download

**Original dataset**: `https://www.kaggle.com/datasets/nexuswho/laboro-tomato`

This repo hosts structure and conversion scripts only; place the downloaded folders under this directory.

**Local license file**: See `LICENSE` in the root directory.

## Dataset Structure

```
tomato_ripeness_detection/
├── tomatoes/                              # Main category directory
│   ├── csv/                              # CSV annotation files (per-image)
│   ├── json/                              # JSON annotation files (per-image, optional)
│   ├── images/                            # Image files
│   ├── labelmap.json                     # Label mapping file
│   └── sets/                              # Dataset split files
│       ├── train.txt                     # Training set image list
│       ├── val.txt                       # Validation set image list
│       ├── test.txt                      # Test set image list
│       ├── all.txt                        # All images list
│       └── train_val.txt                  # Train+val images list
│
├── annotations/                           # COCO format JSON files (generated)
│   ├── tomatoes_instances_train.json
│   ├── tomatoes_instances_val.json
│   └── tomatoes_instances_test.json
│
├── scripts/                               # Utility scripts
│   ├── reorganize_dataset.py              # Reorganize dataset to standard structure
│   └── convert_to_coco.py                 # Convert CSV to COCO format
│
├── LICENSE                                # License file
├── README.md                              # This file
└── requirements.txt                       # Python dependencies
```

**Splits**: Splits provided via `tomatoes/sets/*.txt`. List image basenames (no extension). If missing, all images are used.

## Sample Images

<table>
  <tr>
    <th>Category</th>
    <th>Sample</th>
  </tr>
  <tr>
    <td><strong>Fully Ripened Tomato</strong></td>
    <td>
      <img src="tomatoes/images/IMG_20191215_112926.jpg" alt="Fully ripened tomato" width="260"/>
      <div align="center"><code>tomatoes/images/IMG_20191215_112926.jpg</code></div>
    </td>
  </tr>
  <tr>
    <td><strong>Half Ripened Tomato</strong></td>
    <td>
      <img src="tomatoes/images/IMG_20191215_111605.jpg" alt="Half ripened tomato" width="260"/>
      <div align="center"><code>tomatoes/images/IMG_20191215_111605.jpg</code></div>
    </td>
  </tr>
  <tr>
    <td><strong>Green Tomato</strong></td>
    <td>
      <img src="tomatoes/images/IMG_20191215_111751.jpg" alt="Green tomato" width="260"/>
      <div align="center"><code>tomatoes/images/IMG_20191215_111751.jpg</code></div>
    </td>
  </tr>
</table>

## Annotation Schema

### CSV Format

Each image has a corresponding CSV annotation file in `tomatoes/csv/{image_name}.csv`:

```csv
#item,x,y,width,height,label
0,107.37,48.42,22.0,22.0,1
1,233.16,217.37,24.0,24.0,2
```

- **Coordinates**: `x, y` - top-left corner of bounding box (pixels)
- **Dimensions**: `width, height` - bounding box dimensions (pixels)
- **Label**: Category ID (1=b_fully_ripened, 2=b_half_ripened, 3=b_green, 4=l_fully_ripened, 5=l_half_ripened, 6=l_green)

### COCO Format

COCO format JSON files are generated in the `annotations/` directory. Example structure:

```json
{
  "info": {
    "year": 2020,
    "version": "2.0",
    "description": "Tomato Ripeness Detection tomatoes train split",
    "url": "https://laboro.ai/",
    "contributor": "Laboro.ai"
  },
  "images": [
    {
      "id": 1,
      "file_name": "tomatoes/images/IMG_20191215_112926.jpg",
      "width": 3120,
      "height": 4160
    }
  ],
  "annotations": [
    {
      "id": 1,
      "image_id": 1,
      "category_id": 1,
      "bbox": [107.37, 48.42, 22.0, 22.0],
      "area": 484.0,
      "iscrowd": 0
    }
  ],
  "categories": [
    {
      "id": 1,
      "name": "b_fully_ripened",
      "supercategory": "tomato_ripeness"
    },
    {
      "id": 2,
      "name": "b_half_ripened",
      "supercategory": "tomato_ripeness"
    },
    {
      "id": 3,
      "name": "b_green",
      "supercategory": "tomato_ripeness"
    },
    {
      "id": 4,
      "name": "l_fully_ripened",
      "supercategory": "tomato_ripeness"
    },
    {
      "id": 5,
      "name": "l_half_ripened",
      "supercategory": "tomato_ripeness"
    },
    {
      "id": 6,
      "name": "l_green",
      "supercategory": "tomato_ripeness"
    }
  ],
  "licenses": [
    {
      "id": 1,
      "name": "Attribution-NonCommercial-ShareAlike License",
      "url": "http://creativecommons.org/licenses/by-nc-sa/4.0/"
    }
  ]
}
```

### Label Maps

Label mapping is defined in `tomatoes/labelmap.json`:

```json
[
  {"object_id": 0, "label_id": 0, "keyboard_shortcut": "0", "object_name": "background"},
  {"object_id": 1, "label_id": 1, "keyboard_shortcut": "1", "object_name": "b_fully_ripened"},
  {"object_id": 2, "label_id": 2, "keyboard_shortcut": "2", "object_name": "b_half_ripened"},
  {"object_id": 3, "label_id": 3, "keyboard_shortcut": "3", "object_name": "b_green"},
  {"object_id": 4, "label_id": 4, "keyboard_shortcut": "4", "object_name": "l_fully_ripened"},
  {"object_id": 5, "label_id": 5, "keyboard_shortcut": "5", "object_name": "l_half_ripened"},
  {"object_id": 6, "label_id": 6, "keyboard_shortcut": "6", "object_name": "l_green"}
]
```

## Stats and Splits

### Image Statistics

- **Total images**: 804
- **Training set**: 643 images (80%)
- **Validation set**: 161 images (20%)
- **Test set**: 161 images (same as validation set)

### Annotation Statistics

- **Total annotations**: 9,777
- **Training annotations**: 7,781
- **Validation annotations**: 1,996
- **Test annotations**: 1,996

### Categories

1. **b_fully_ripened**: Fully ripened tomato
2. **b_half_ripened**: Half-ripened tomato
3. **b_green**: Green tomato
4. **l_fully_ripened**: Fully ripened leaf
5. **l_half_ripened**: Half-ripened leaf
6. **l_green**: Green leaf

Splits provided via `tomatoes/sets/*.txt`. You may define your own splits by editing those files.

## Quick Start

### Convert to COCO Format

```bash
python scripts/convert_to_coco.py --root . --out annotations --category tomatoes --splits train val test
```

### Load with COCO API

```python
from pycocotools.coco import COCO
import matplotlib.pyplot as plt

# Load annotations
coco = COCO('annotations/tomatoes_instances_train.json')

# Get image IDs
img_ids = coco.getImgIds()
print(f"Number of images: {len(img_ids)}")

# Get category IDs
cat_ids = coco.getCatIds()
print(f"Categories: {coco.loadCats(cat_ids)}")

# Load and display an image with annotations
img_id = img_ids[0]
img_info = coco.loadImgs(img_id)[0]
ann_ids = coco.getAnnIds(imgIds=img_id)
anns = coco.loadAnns(ann_ids)

# Display image
img = plt.imread(img_info['file_name'])
plt.imshow(img)
coco.showAnns(anns)
plt.show()
```

### Dependencies

**Required**:
- Pillow>=9.5

**Optional** (for COCO API):
- pycocotools>=2.0.7

Install with:
```bash
pip install -r requirements.txt
```

## Evaluation and Baselines

### Evaluation Metrics

- **mAP@[.50:.95]**: Mean Average Precision at IoU thresholds from 0.50 to 0.95
- **mAP@0.50**: Mean Average Precision at IoU threshold 0.50
- **mAP@0.75**: Mean Average Precision at IoU threshold 0.75

### Baseline Results

(To be added based on experimental results)

## Datasheet (Data Card)

### Motivation

This dataset was created to support research in automated tomato ripeness detection and classification for agricultural applications, including precision agriculture, crop yield prediction, and automated harvesting systems.

### Composition

The dataset contains:
- **Images**: 804 high-resolution RGB images of tomatoes and leaves
- **Categories**: 6 ripeness/health stages (3 for tomatoes, 3 for leaves)
- **Annotations**: Bounding box annotations in CSV and COCO formats
- **Splits**: Training (643), validation (161), and test (161) sets

### Collection Process

- Images were collected from real-world agricultural settings
- Original dataset from Laboro.ai (2020)
- Images captured using various camera devices and lighting conditions
- Annotations converted from YOLO format to CSV and COCO formats

### Preprocessing

- Images organized into standard directory structure
- YOLO format annotations converted to CSV format (pixel coordinates)
- COCO format JSON files generated from CSV annotations
- Dataset splits created (train/val/test)

### Distribution

The dataset is distributed via Kaggle: `https://www.kaggle.com/datasets/nexuswho/laboro-tomato`

### Maintenance

This standardized structure is maintained to ensure consistency with other agricultural datasets. Updates and improvements are tracked in the changelog.

## Known Issues and Caveats

1. **Coordinate System**: Bounding boxes use top-left corner coordinates `[x, y, width, height]` in pixel units.

2. **File Naming**: Image files use naming patterns like `IMG_YYYYMMDD_HHMMSS.jpg` or `IMG_####.jpg`.

3. **Image Formats**: Images are primarily in JPEG format, with variable resolutions.

4. **Test Set**: The test set is currently the same as the validation set. Consider creating a separate test set for final evaluation.

5. **Category Naming**: Category names use prefixes:
   - `b_` for tomato (berry) categories
   - `l_` for leaf categories

6. **License**: The original dataset uses CC BY-NC-SA 4.0 license. Please check the original dataset terms and cite appropriately.

## License

This dataset is licensed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0)**.

**Key terms**:
- **Attribution**: You must give appropriate credit
- **NonCommercial**: You may not use the material for commercial purposes
- **ShareAlike**: If you remix, transform, or build upon the material, you must distribute your contributions under the same license

Check the original dataset terms and cite appropriately. See `LICENSE` file for full license text.

## Citation

If you use this dataset, please cite:

```bibtex
@dataset{tomato_ripeness_detection_2020,
  title={Tomato Ripeness Detection Dataset},
  author={Laboro.ai},
  year={2020},
  url={https://www.kaggle.com/datasets/nexuswho/laboro-tomato},
  license={CC BY-NC-SA 4.0}
}
```

## Changelog

- **V1.0.0** (2025): Initial standardized structure and COCO conversion utility
  - Reorganized dataset to standard directory structure
  - Converted YOLO format annotations to CSV format
  - Generated COCO format JSON files
  - Created dataset split files
  - Added conversion scripts

## Contact

- **Maintainers**: Dataset structure maintained for standardization
- **Original Authors**: Laboro.ai
- **Source**: `https://www.kaggle.com/datasets/nexuswho/laboro-tomato`
- **Original Dataset**: `https://laboro.ai/`
