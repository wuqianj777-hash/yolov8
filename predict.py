<<<<<<< HEAD
from ultralytics import YOLO

if __name__ == '__main__':
    # 加载训练好的最优模型
    model = YOLO('runs/train/drone_exp3/weights/best.pt')

    # 单张图片检测
    results = model.predict(
        source='D:/yolov8/new-yolov8/ultralytics-main/datasets/images/test',  # 改成你的测试图片/视频路径
        save=True,  # 保存结果图
        conf=0.25,  # 置信度阈值
        show=True  # 是否弹窗显示
=======
from ultralytics import YOLO

if __name__ == '__main__':
    # 加载训练好的最优模型
    model = YOLO('runs/train/drone_exp3/weights/best.pt')

    # 单张图片检测
    results = model.predict(
        source='D:/yolov8/new-yolov8/ultralytics-main/datasets/images/test',  # 改成你的测试图片/视频路径
        save=True,  # 保存结果图
        conf=0.25,  # 置信度阈值
        show=True  # 是否弹窗显示
>>>>>>> 02646c286ff348358fce6a3dafefa5a2a2334056
    )