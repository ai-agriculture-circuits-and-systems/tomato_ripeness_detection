# 原始数据说明

本目录包含数据集的原始数据文件，保留原始格式和结构。

## 目录结构

```
data/origin/
├── train/                    # 训练集原始数据
│   ├── images/               # 训练图像
│   └── labels/               # YOLO格式标注文件
├── val/                      # 验证集原始数据
│   ├── images/               # 验证图像
│   └── labels/               # YOLO格式标注文件
└── example_dataset.yaml      # YOLO数据集配置文件
```

## YAML 配置文件说明

`example_dataset.yaml` 是用于 YOLO 训练的数据集配置文件，包含以下内容：

### 文件内容

```yaml
names:
  - b_fully_ripened      # 完全成熟的番茄
  - b_half_ripened       # 半成熟的番茄
  - b_green              # 绿色番茄
  - l_fully_ripened      # 完全成熟的叶子
  - l_half_ripened       # 半成熟的叶子
  - l_green              # 绿色叶子
nc: 6                    # 类别数量
path: D:\Datasets\laboro_tomato    # 数据集路径（原始路径，已更新）
train: train\images      # 训练集图像路径
val: val\images          # 验证集图像路径
```

### 字段说明

- **names**: 类别名称列表，定义了6个类别
  - `b_` 前缀表示番茄（berry）类别
  - `l_` 前缀表示叶子（leaf）类别
- **nc**: 类别数量（number of classes），值为6
- **path**: 数据集根目录路径（原始路径为 Windows 路径，已不再使用）
- **train**: 训练集图像目录的相对路径
- **val**: 验证集图像目录的相对路径

### 用途

这个 YAML 文件主要用于：
1. **YOLO 训练配置**: 在 YOLOv5/YOLOv8 等框架中训练模型时，需要此配置文件来指定类别和路径
2. **数据集元数据**: 记录数据集的类别信息和组织结构
3. **脚本参考**: 其他脚本可以读取此文件来获取类别信息

### 使用示例

在 YOLO 训练中使用：

```bash
# YOLOv5
python train.py --data data/origin/example_dataset.yaml --img 640 --batch 16 --epochs 100

# YOLOv8
yolo detect train data=data/origin/example_dataset.yaml model=yolov8n.pt epochs=100
```

使用 Python 脚本读取：

```python
import yaml

with open('data/origin/example_dataset.yaml', 'r') as f:
    config = yaml.safe_load(f)
    
print(f"类别数量: {config['nc']}")
print(f"类别名称: {config['names']}")
```

### 注意事项

- 原始路径 `path: D:\Datasets\laboro_tomato` 是 Windows 路径，已不再使用
- 实际使用时，路径应该相对于数据集根目录或使用绝对路径
- 标准化后的数据集结构位于 `tomatoes/` 目录下，使用 CSV 和 COCO 格式




