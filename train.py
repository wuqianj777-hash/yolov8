<<<<<<< HEAD
import warnings

warnings.filterwarnings('ignore')
from ultralytics import YOLO

if __name__ == '__main__':
    # 加载预训练模型（新手推荐用预训练权重，收敛更快效果更好）
    model = YOLO('yolov8n.pt')

    # 开始训练
    model.train(
        data='data.yaml',  # 第三步的数据集配置文件
        imgsz=960,  # 输入图片尺寸，显存够可以开800/960提升小目标效果
        epochs=150,  # 训练轮数，小数据集100-200足够
        batch=4,  # 批次大小，显存不够就调小（2/4/8）
        workers=0,  # Windows系统建议设0，避免多线程报错
        device=0,  # 用第0块GPU，没有GPU就写'cpu'
        optimizer='SGD',  # 优化器，也可以用Adam
        close_mosaic=10,  # 最后10轮关闭马赛克增强，稳定精度
        resume=False,  # 中断续训练设True
        project='runs/train',  # 结果保存目录
        name='drone_exp',  # 本次实验文件夹名
        single_cls=False,  # 单类别也可以设True
        cache=False,
=======
import warnings

warnings.filterwarnings('ignore')
from ultralytics import YOLO

if __name__ == '__main__':
    # 加载预训练模型（新手推荐用预训练权重，收敛更快效果更好）
    model = YOLO('yolov8n.pt')

    # 开始训练
    model.train(
        data='data.yaml',  # 第三步的数据集配置文件
        imgsz=960,  # 输入图片尺寸，显存够可以开800/960提升小目标效果
        epochs=150,  # 训练轮数，小数据集100-200足够
        batch=4,  # 批次大小，显存不够就调小（2/4/8）
        workers=0,  # Windows系统建议设0，避免多线程报错
        device=0,  # 用第0块GPU，没有GPU就写'cpu'
        optimizer='SGD',  # 优化器，也可以用Adam
        close_mosaic=10,  # 最后10轮关闭马赛克增强，稳定精度
        resume=False,  # 中断续训练设True
        project='runs/train',  # 结果保存目录
        name='drone_exp',  # 本次实验文件夹名
        single_cls=False,  # 单类别也可以设True
        cache=False,
>>>>>>> 02646c286ff348358fce6a3dafefa5a2a2334056
    )