import os
import random
import shutil

def split_dataset():
    img_dir = r"D:\AHyper_data\data2\drone_duzhenyu\output"
    label_dir = r"D:\AHyper_data\data2\drone_duzhenyu\label"
    output_dir = r"E:\Users\Serendipity\Desktop\yolov8\new-yolov8\ultralytics-main\ultralytics\data2"
    ratios = (0.8, 0.1, 0.1)

    if not os.path.exists(img_dir) or not os.path.exists(label_dir):
        print("错误：找不到 output 或 label 文件夹"); return

    for split in ['train', 'val', 'test']:
        os.makedirs(os.path.join(output_dir, split, 'images'), exist_ok=True)
        os.makedirs(os.path.join(output_dir, split, 'labels'), exist_ok=True)

    img_files = [f for f in os.listdir(img_dir) if f.lower().endswith('.png')]
    base_names = [os.path.splitext(f)[0] for f in img_files]
    random.shuffle(base_names)
    
    total = len(base_names)
    train_end = int(total * ratios[0])
    val_end = train_end + int(total * ratios[1])

    split_map = {
        'train': base_names[:train_end],
        'val': base_names[train_end:val_end],
        'test': base_names[val_end:]
    }

    for split, names in split_map.items():
        print(f"处理 {split} 集: {len(names)} 个样本")
        for name in names:
            shutil.copy(f"{img_dir}/{name}.png", f"{output_dir}/{split}/images/{name}.png")
            shutil.copy(f"{label_dir}/{name}.txt", f"{output_dir}/{split}/labels/{name}.txt")

    print("数据集整理完成！位置：./datasets")

if __name__ == '__main__':
    random.seed(42)
    split_dataset()