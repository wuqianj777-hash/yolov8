<<<<<<< HEAD
import os
import shutil
from sklearn.model_selection import train_test_split
from pathlib import Path

# ========== 修改这里的路径 ==========
img_path = r"C:\Users\24324\Desktop\newfig"   # 原始图片文件夹
txt_path = r"C:\Users\24324\Desktop\newlabel"   # 原始标签文件夹
output_dir = Path(r"C:\Users\24324\Desktop\datasets")  # 划分后输出目录
# ====================================

# 数据集比例：训练70%，验证20%，测试10%
val_ratio = 0.2
test_ratio = 0.1

# 创建目录结构
folders = {
    'train': {'img': output_dir/'images'/'train', 'lbl': output_dir/'labels'/'train'},
    'val':   {'img': output_dir/'images'/'val',   'lbl': output_dir/'labels'/'val'},
    'test':  {'img': output_dir/'images'/'test',  'lbl': output_dir/'labels'/'test'},
}
for f in folders.values():
    f['img'].mkdir(parents=True, exist_ok=True)
    f['lbl'].mkdir(parents=True, exist_ok=True)

# 获取所有图片文件名
img_list = [f for f in os.listdir(img_path) if f.lower().endswith(('.jpg','.jpeg','.png'))]
name_list = [os.path.splitext(f)[0] for f in img_list]

# 划分：先分训练+验证 vs 测试，再分训练 vs 验证
train_val_names, test_names = train_test_split(name_list, test_size=test_ratio, random_state=42)
train_names, val_names = train_test_split(train_val_names, test_size=val_ratio/(1-test_ratio), random_state=42)

# 复制文件
def copy_files(name_list, split):
    for name in name_list:
        # 找对应图片
        for ext in ['.jpg', '.jpeg', '.png']:
            img_file = os.path.join(img_path, name + ext)
            if os.path.exists(img_file):
                shutil.copy(img_file, folders[split]['img'] / (name + ext))
                break
        # 复制标签
        txt_file = os.path.join(txt_path, name + '.txt')
        if os.path.exists(txt_file):
            shutil.copy(txt_file, folders[split]['lbl'] / (name + '.txt'))

copy_files(train_names, 'train')
copy_files(val_names, 'val')
copy_files(test_names, 'test')

=======
import os
import shutil
from sklearn.model_selection import train_test_split
from pathlib import Path

# ========== 修改这里的路径 ==========
img_path = r"C:\Users\24324\Desktop\newfig"   # 原始图片文件夹
txt_path = r"C:\Users\24324\Desktop\newlabel"   # 原始标签文件夹
output_dir = Path(r"C:\Users\24324\Desktop\datasets")  # 划分后输出目录
# ====================================

# 数据集比例：训练70%，验证20%，测试10%
val_ratio = 0.2
test_ratio = 0.1

# 创建目录结构
folders = {
    'train': {'img': output_dir/'images'/'train', 'lbl': output_dir/'labels'/'train'},
    'val':   {'img': output_dir/'images'/'val',   'lbl': output_dir/'labels'/'val'},
    'test':  {'img': output_dir/'images'/'test',  'lbl': output_dir/'labels'/'test'},
}
for f in folders.values():
    f['img'].mkdir(parents=True, exist_ok=True)
    f['lbl'].mkdir(parents=True, exist_ok=True)

# 获取所有图片文件名
img_list = [f for f in os.listdir(img_path) if f.lower().endswith(('.jpg','.jpeg','.png'))]
name_list = [os.path.splitext(f)[0] for f in img_list]

# 划分：先分训练+验证 vs 测试，再分训练 vs 验证
train_val_names, test_names = train_test_split(name_list, test_size=test_ratio, random_state=42)
train_names, val_names = train_test_split(train_val_names, test_size=val_ratio/(1-test_ratio), random_state=42)

# 复制文件
def copy_files(name_list, split):
    for name in name_list:
        # 找对应图片
        for ext in ['.jpg', '.jpeg', '.png']:
            img_file = os.path.join(img_path, name + ext)
            if os.path.exists(img_file):
                shutil.copy(img_file, folders[split]['img'] / (name + ext))
                break
        # 复制标签
        txt_file = os.path.join(txt_path, name + '.txt')
        if os.path.exists(txt_file):
            shutil.copy(txt_file, folders[split]['lbl'] / (name + '.txt'))

copy_files(train_names, 'train')
copy_files(val_names, 'val')
copy_files(test_names, 'test')

>>>>>>> 02646c286ff348358fce6a3dafefa5a2a2334056
print(f"划分完成：训练集{len(train_names)}张，验证集{len(val_names)}张，测试集{len(test_names)}张")