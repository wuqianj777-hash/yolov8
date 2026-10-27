<<<<<<< HEAD
import cv2
import os
import numpy as np
from pathlib import Path

def crop_and_update_yolo(img_dir, label_dir, output_img_dir, output_label_dir, target_size=(1080, 1080)):
    """
    裁剪图像并更新YOLO标注
    
    参数:
        img_dir: 原始图像目录
        label_dir: 原始标签目录
        output_img_dir: 输出图像目录
        output_label_dir: 输出标签目录
        target_size: 目标尺寸 (width, height)
    """
    # 创建输出目录
    os.makedirs(output_img_dir, exist_ok=True)
    os.makedirs(output_label_dir, exist_ok=True)
    
    # 获取所有图像文件
    img_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    img_files = []
    for ext in img_extensions:
        img_files.extend(list(Path(img_dir).glob(f'*{ext}')))
        img_files.extend(list(Path(img_dir).glob(f'*{ext.upper()}')))
    
    print(f"找到 {len(img_files)} 个图像文件")
    
    for img_path in img_files:
        # 读取图像
        img = cv2.imread(str(img_path))
        if img is None:
            print(f"无法读取图像: {img_path}")
            continue
        
        h, w = img.shape[:2]
        print(f"处理: {img_path.name}, 原始尺寸: {w}x{h}")
        
        # 检查图像尺寸
        if w != 1920 or h != 1080:
            print(f"警告: 图像 {img_path.name} 尺寸不是1920x1080，而是 {w}x{h}")
        
        # 读取对应的标签文件
        label_path = Path(label_dir) / f"{img_path.stem}.txt"
        if not label_path.exists():
            print(f"警告: 找不到标签文件 {label_path}")
            continue
        
        # 读取YOLO标注
        with open(label_path, 'r') as f:
            lines = f.readlines()
        
        # 解析标注
        boxes = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) != 5:
                continue
            class_id, x_center, y_center, width, height = map(float, parts)
            boxes.append([class_id, x_center, y_center, width, height])
        
        if not boxes:
            print(f"警告: 标签文件 {label_path} 中没有有效标注")
            continue
        
        # 计算裁剪区域（水平方向居中裁剪，因为1920->1080需要裁剪两侧）
        target_w, target_h = target_size
        
        # 计算裁剪的起始点（水平方向居中裁剪）
        x_start = (w - target_w) // 2  # 对于1920x1080，裁剪两侧各420像素
        x_end = x_start + target_w
        y_start = 0  # 高度已经是1080，不需要裁剪
        y_end = h
        
        print(f"  裁剪区域: x=[{x_start}, {x_end}], y=[{y_start}, {y_end}]")
        
        # 检查并过滤在裁剪区域内的目标
        valid_boxes = []
        for box in boxes:
            class_id, x_center, y_center, width, height = box
            
            # 转换到绝对坐标
            abs_x_center = x_center * w
            abs_y_center = y_center * h
            abs_width = width * w
            abs_height = height * h
            
            # 计算边界框的四个角点
            x_min = abs_x_center - abs_width / 2
            x_max = abs_x_center + abs_width / 2
            y_min = abs_y_center - abs_height / 2
            y_max = abs_y_center + abs_height / 2
            
            # 检查是否在裁剪区域内
            # 允许部分在裁剪区域内（只要有一部分在就行）
            overlap_x_min = max(x_min, x_start)
            overlap_x_max = min(x_max, x_end)
            overlap_y_min = max(y_min, y_start)
            overlap_y_max = min(y_max, y_end)
            
            # 如果有重叠部分
            if overlap_x_min < overlap_x_max and overlap_y_min < overlap_y_max:
                # 计算重叠部分的中心点和尺寸
                overlap_width = overlap_x_max - overlap_x_min
                overlap_height = overlap_y_max - overlap_y_min
                
                # 只有当重叠部分足够大时才保留（至少50%的IoU）
                original_area = abs_width * abs_height
                overlap_area = overlap_width * overlap_height
                iou_ratio = overlap_area / original_area if original_area > 0 else 0
                
                if iou_ratio >= 0.5:  # 至少保留50%的目标
                    # 更新坐标到新图像坐标系
                    new_x_center = (overlap_x_min + overlap_x_max) / 2 - x_start
                    new_y_center = (overlap_y_min + overlap_y_max) / 2 - y_start
                    
                    # 归一化到新图像尺寸
                    new_x_center /= target_w
                    new_y_center /= target_h
                    new_width = overlap_width / target_w
                    new_height = overlap_height / target_h
                    
                    # 确保坐标在[0,1]范围内
                    new_x_center = max(0.0, min(1.0, new_x_center))
                    new_y_center = max(0.0, min(1.0, new_y_center))
                    new_width = max(0.0, min(1.0, new_width))
                    new_height = max(0.0, min(1.0, new_height))
                    
                    valid_boxes.append([class_id, new_x_center, new_y_center, new_width, new_height])
                    print(f"  目标保留: 类别={int(class_id)}, IoU={iou_ratio:.2f}")
                else:
                    print(f"  目标被裁剪过多(IoU={iou_ratio:.2f})，已丢弃")
        
        # 如果没有有效目标，跳过该图像
        if not valid_boxes:
            print(f"警告: {img_path.name} 没有有效目标在裁剪区域内，已跳过")
            continue
        
        # 裁剪图像
        cropped_img = img[y_start:y_end, x_start:x_end]
        
        # 验证裁剪后的尺寸
        cropped_h, cropped_w = cropped_img.shape[:2]
        if cropped_w != target_w or cropped_h != target_h:
            print(f"错误: 裁剪后尺寸不正确: {cropped_w}x{cropped_h}，期望: {target_w}x{target_h}")
            continue
        
        # 保存裁剪后的图像
        output_img_path = Path(output_img_dir) / img_path.name
        cv2.imwrite(str(output_img_path), cropped_img)
        
        # 保存更新后的标签
        output_label_path = Path(output_label_dir) / f"{img_path.stem}.txt"
        with open(output_label_path, 'w') as f:
            for box in valid_boxes:
                class_id, x_center, y_center, width, height = box
                f.write(f"{int(class_id)} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
        
        print(f"✓ 处理完成: {img_path.name} -> 保存为 {output_img_path.name}")

def main():
    # 配置路径
    img_dir = r"C:\Users\24324\Desktop\img"  # 原始图像目录
    label_dir = r"C:\Users\24324\Desktop\label"  # 原始标签目录
    output_img_dir = r"C:\Users\24324\Desktop\newfig"  # 输出图像目录
    output_label_dir = r"C:\Users\24324\Desktop\newlabel"  # 输出标签目录
    
    print("=" * 60)
    print("开始处理数据集...")
    print(f"输入图像目录: {img_dir}")
    print(f"输入标签目录: {label_dir}")
    print(f"输出图像目录: {output_img_dir}")
    print(f"输出标签目录: {output_label_dir}")
    print("=" * 60)
    
    # 运行裁剪和更新
    crop_and_update_yolo(
        img_dir=img_dir,
        label_dir=label_dir,
        output_img_dir=output_img_dir,
        output_label_dir=output_label_dir,
        target_size=(1080, 1080)  # 修改为1080x1080
    )
    
    print("=" * 60)
    print("处理完成！")
    print("=" * 60)

if __name__ == "__main__":
=======
import cv2
import os
import numpy as np
from pathlib import Path

def crop_and_update_yolo(img_dir, label_dir, output_img_dir, output_label_dir, target_size=(1080, 1080)):
    """
    裁剪图像并更新YOLO标注
    
    参数:
        img_dir: 原始图像目录
        label_dir: 原始标签目录
        output_img_dir: 输出图像目录
        output_label_dir: 输出标签目录
        target_size: 目标尺寸 (width, height)
    """
    # 创建输出目录
    os.makedirs(output_img_dir, exist_ok=True)
    os.makedirs(output_label_dir, exist_ok=True)
    
    # 获取所有图像文件
    img_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    img_files = []
    for ext in img_extensions:
        img_files.extend(list(Path(img_dir).glob(f'*{ext}')))
        img_files.extend(list(Path(img_dir).glob(f'*{ext.upper()}')))
    
    print(f"找到 {len(img_files)} 个图像文件")
    
    for img_path in img_files:
        # 读取图像
        img = cv2.imread(str(img_path))
        if img is None:
            print(f"无法读取图像: {img_path}")
            continue
        
        h, w = img.shape[:2]
        print(f"处理: {img_path.name}, 原始尺寸: {w}x{h}")
        
        # 检查图像尺寸
        if w != 1920 or h != 1080:
            print(f"警告: 图像 {img_path.name} 尺寸不是1920x1080，而是 {w}x{h}")
        
        # 读取对应的标签文件
        label_path = Path(label_dir) / f"{img_path.stem}.txt"
        if not label_path.exists():
            print(f"警告: 找不到标签文件 {label_path}")
            continue
        
        # 读取YOLO标注
        with open(label_path, 'r') as f:
            lines = f.readlines()
        
        # 解析标注
        boxes = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) != 5:
                continue
            class_id, x_center, y_center, width, height = map(float, parts)
            boxes.append([class_id, x_center, y_center, width, height])
        
        if not boxes:
            print(f"警告: 标签文件 {label_path} 中没有有效标注")
            continue
        
        # 计算裁剪区域（水平方向居中裁剪，因为1920->1080需要裁剪两侧）
        target_w, target_h = target_size
        
        # 计算裁剪的起始点（水平方向居中裁剪）
        x_start = (w - target_w) // 2  # 对于1920x1080，裁剪两侧各420像素
        x_end = x_start + target_w
        y_start = 0  # 高度已经是1080，不需要裁剪
        y_end = h
        
        print(f"  裁剪区域: x=[{x_start}, {x_end}], y=[{y_start}, {y_end}]")
        
        # 检查并过滤在裁剪区域内的目标
        valid_boxes = []
        for box in boxes:
            class_id, x_center, y_center, width, height = box
            
            # 转换到绝对坐标
            abs_x_center = x_center * w
            abs_y_center = y_center * h
            abs_width = width * w
            abs_height = height * h
            
            # 计算边界框的四个角点
            x_min = abs_x_center - abs_width / 2
            x_max = abs_x_center + abs_width / 2
            y_min = abs_y_center - abs_height / 2
            y_max = abs_y_center + abs_height / 2
            
            # 检查是否在裁剪区域内
            # 允许部分在裁剪区域内（只要有一部分在就行）
            overlap_x_min = max(x_min, x_start)
            overlap_x_max = min(x_max, x_end)
            overlap_y_min = max(y_min, y_start)
            overlap_y_max = min(y_max, y_end)
            
            # 如果有重叠部分
            if overlap_x_min < overlap_x_max and overlap_y_min < overlap_y_max:
                # 计算重叠部分的中心点和尺寸
                overlap_width = overlap_x_max - overlap_x_min
                overlap_height = overlap_y_max - overlap_y_min
                
                # 只有当重叠部分足够大时才保留（至少50%的IoU）
                original_area = abs_width * abs_height
                overlap_area = overlap_width * overlap_height
                iou_ratio = overlap_area / original_area if original_area > 0 else 0
                
                if iou_ratio >= 0.5:  # 至少保留50%的目标
                    # 更新坐标到新图像坐标系
                    new_x_center = (overlap_x_min + overlap_x_max) / 2 - x_start
                    new_y_center = (overlap_y_min + overlap_y_max) / 2 - y_start
                    
                    # 归一化到新图像尺寸
                    new_x_center /= target_w
                    new_y_center /= target_h
                    new_width = overlap_width / target_w
                    new_height = overlap_height / target_h
                    
                    # 确保坐标在[0,1]范围内
                    new_x_center = max(0.0, min(1.0, new_x_center))
                    new_y_center = max(0.0, min(1.0, new_y_center))
                    new_width = max(0.0, min(1.0, new_width))
                    new_height = max(0.0, min(1.0, new_height))
                    
                    valid_boxes.append([class_id, new_x_center, new_y_center, new_width, new_height])
                    print(f"  目标保留: 类别={int(class_id)}, IoU={iou_ratio:.2f}")
                else:
                    print(f"  目标被裁剪过多(IoU={iou_ratio:.2f})，已丢弃")
        
        # 如果没有有效目标，跳过该图像
        if not valid_boxes:
            print(f"警告: {img_path.name} 没有有效目标在裁剪区域内，已跳过")
            continue
        
        # 裁剪图像
        cropped_img = img[y_start:y_end, x_start:x_end]
        
        # 验证裁剪后的尺寸
        cropped_h, cropped_w = cropped_img.shape[:2]
        if cropped_w != target_w or cropped_h != target_h:
            print(f"错误: 裁剪后尺寸不正确: {cropped_w}x{cropped_h}，期望: {target_w}x{target_h}")
            continue
        
        # 保存裁剪后的图像
        output_img_path = Path(output_img_dir) / img_path.name
        cv2.imwrite(str(output_img_path), cropped_img)
        
        # 保存更新后的标签
        output_label_path = Path(output_label_dir) / f"{img_path.stem}.txt"
        with open(output_label_path, 'w') as f:
            for box in valid_boxes:
                class_id, x_center, y_center, width, height = box
                f.write(f"{int(class_id)} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
        
        print(f"✓ 处理完成: {img_path.name} -> 保存为 {output_img_path.name}")

def main():
    # 配置路径
    img_dir = r"C:\Users\24324\Desktop\img"  # 原始图像目录
    label_dir = r"C:\Users\24324\Desktop\label"  # 原始标签目录
    output_img_dir = r"C:\Users\24324\Desktop\newfig"  # 输出图像目录
    output_label_dir = r"C:\Users\24324\Desktop\newlabel"  # 输出标签目录
    
    print("=" * 60)
    print("开始处理数据集...")
    print(f"输入图像目录: {img_dir}")
    print(f"输入标签目录: {label_dir}")
    print(f"输出图像目录: {output_img_dir}")
    print(f"输出标签目录: {output_label_dir}")
    print("=" * 60)
    
    # 运行裁剪和更新
    crop_and_update_yolo(
        img_dir=img_dir,
        label_dir=label_dir,
        output_img_dir=output_img_dir,
        output_label_dir=output_label_dir,
        target_size=(1080, 1080)  # 修改为1080x1080
    )
    
    print("=" * 60)
    print("处理完成！")
    print("=" * 60)

if __name__ == "__main__":
>>>>>>> 02646c286ff348358fce6a3dafefa5a2a2334056
    main()