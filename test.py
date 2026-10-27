<<<<<<< HEAD
"""
YOLOv8 权重测试脚本
功能：验证本地 yolov8n.pt 权重文件是否正常工作
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径（如果需要）
# current_dir = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(str(Path(current_dir).parent))

def test_yolov8_weights():
    """测试 YOLOv8 权重文件"""
    
    print("=" * 60)
    print("YOLOv8 权重测试开始")
    print("=" * 60)
    
    # 1. 检查权重文件是否存在
    weight_path = "yolov8_pt/yolov8n.pt"
    
    if not os.path.exists(weight_path):
        print(f"❌ 错误：权重文件不存在于 {weight_path}")
        print("请确认文件路径是否正确")
        return False
    
    print(f"✅ 找到权重文件: {weight_path}")
    print(f"   文件大小: {os.path.getsize(weight_path) / (1024 * 1024):.2f} MB")
    
    # 2. 检查 PyTorch 环境
    try:
        import torch
        print(f"✅ PyTorch 版本: {torch.__version__}")
        print(f"✅ CUDA 可用: {torch.cuda.is_available()}")
        
        if torch.cuda.is_available():
            print(f"✅ GPU 名称: {torch.cuda.get_device_name(0)}")
            print(f"✅ CUDA 算力: {torch.cuda.get_device_capability()}")
    except ImportError as e:
        print(f"❌ PyTorch 导入失败: {e}")
        return False
    
    # 3. 测试加载 YOLOv8 模型
    try:
        from ultralytics import YOLO
        
        print("\n正在加载模型...")
        model = YOLO(weight_path)
        print("✅ 模型加载成功!")
        
        # 打印模型信息
        print(f"\n模型信息:")
        print(f"  类型: {type(model).__name__}")
        print(f"  任务: {model.task}")
        print(f"  类别数量: {len(model.names)}")
        
    except Exception as e:
        print(f"❌ 模型加载失败: {e}")
        return False
    
    # 4. 执行推理测试
    try:
        print("\n正在执行推理测试...")
        
        # 使用官方测试图片
        test_image_url = "https://ultralytics.com/images/bus.jpg"
        
        # 运行预测
        results = model.predict(
            source=test_image_url,
            save=True,      # 保存结果图片
            show=False,     # 不显示窗口（适合无界面环境）
            conf=0.25,      # 置信度阈值
            imgsz=640,      # 输入图像尺寸
            verbose=False   # 减少输出
        )
        
        print("✅ 推理完成!")
        
        # 5. 解析并打印结果
        for i, result in enumerate(results):
            boxes = result.boxes
            
            print(f"\n检测结果 #{i+1}:")
            print(f"  检测到 {len(boxes)} 个目标")
            
            if len(boxes) > 0:
                print("  详细检测信息:")
                for j, box in enumerate(boxes):
                    cls_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    xyxy = box.xyxy[0].tolist()
                    
                    class_name = model.names[cls_id]
                    print(f"    目标 {j+1}: {class_name}")
                    print(f"      置信度: {conf:.2%}")
                    print(f"      边界框: [{xyxy[0]:.1f}, {xyxy[1]:.1f}, {xyxy[2]:.1f}, {xyxy[3]:.1f}]")
            
            # 检查是否保存了图片
            if hasattr(result, 'save_dir'):
                print(f"  结果图片保存到: {result.save_dir}")
        
        # 6. 额外测试：使用本地图片（如果存在）
        local_test_images = [
            "test.jpg",
            "test.png",
            "data/images/bus.jpg",
            "ultralytics/assets/bus.jpg"
        ]
        
        for img_path in local_test_images:
            if os.path.exists(img_path):
                print(f"\n使用本地图片测试: {img_path}")
                results_local = model.predict(
                    source=img_path,
                    save=True,
                    show=False,
                    conf=0.25,
                    imgsz=640
                )
                print(f"✅ 本地图片测试成功!")
                break
        else:
            print("\nℹ️ 未找到本地测试图片，仅使用了在线图片")
        
        return True
        
    except Exception as e:
        print(f"❌ 推理测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    success = test_yolov8_weights()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 所有测试通过！YOLOv8 环境配置正确。")
        print("\n你可以开始使用以下命令进行训练:")
        print("  python train.py --weights yolov8_pt/yolov8n.pt --data your_data.yaml")
        print("或者:")
        print("  from ultralytics import YOLO")
        print("  model = YOLO('yolov8_pt/yolov8n.pt')")
        print("  model.train(data='your_data.yaml', epochs=100)")
    else:
        print("❌ 测试未通过，请检查上述错误信息。")
    print("=" * 60)

if __name__ == "__main__":
=======
"""
YOLOv8 权重测试脚本
功能：验证本地 yolov8n.pt 权重文件是否正常工作
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径（如果需要）
# current_dir = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(str(Path(current_dir).parent))

def test_yolov8_weights():
    """测试 YOLOv8 权重文件"""
    
    print("=" * 60)
    print("YOLOv8 权重测试开始")
    print("=" * 60)
    
    # 1. 检查权重文件是否存在
    weight_path = "yolov8_pt/yolov8n.pt"
    
    if not os.path.exists(weight_path):
        print(f"❌ 错误：权重文件不存在于 {weight_path}")
        print("请确认文件路径是否正确")
        return False
    
    print(f"✅ 找到权重文件: {weight_path}")
    print(f"   文件大小: {os.path.getsize(weight_path) / (1024 * 1024):.2f} MB")
    
    # 2. 检查 PyTorch 环境
    try:
        import torch
        print(f"✅ PyTorch 版本: {torch.__version__}")
        print(f"✅ CUDA 可用: {torch.cuda.is_available()}")
        
        if torch.cuda.is_available():
            print(f"✅ GPU 名称: {torch.cuda.get_device_name(0)}")
            print(f"✅ CUDA 算力: {torch.cuda.get_device_capability()}")
    except ImportError as e:
        print(f"❌ PyTorch 导入失败: {e}")
        return False
    
    # 3. 测试加载 YOLOv8 模型
    try:
        from ultralytics import YOLO
        
        print("\n正在加载模型...")
        model = YOLO(weight_path)
        print("✅ 模型加载成功!")
        
        # 打印模型信息
        print(f"\n模型信息:")
        print(f"  类型: {type(model).__name__}")
        print(f"  任务: {model.task}")
        print(f"  类别数量: {len(model.names)}")
        
    except Exception as e:
        print(f"❌ 模型加载失败: {e}")
        return False
    
    # 4. 执行推理测试
    try:
        print("\n正在执行推理测试...")
        
        # 使用官方测试图片
        test_image_url = "https://ultralytics.com/images/bus.jpg"
        
        # 运行预测
        results = model.predict(
            source=test_image_url,
            save=True,      # 保存结果图片
            show=False,     # 不显示窗口（适合无界面环境）
            conf=0.25,      # 置信度阈值
            imgsz=640,      # 输入图像尺寸
            verbose=False   # 减少输出
        )
        
        print("✅ 推理完成!")
        
        # 5. 解析并打印结果
        for i, result in enumerate(results):
            boxes = result.boxes
            
            print(f"\n检测结果 #{i+1}:")
            print(f"  检测到 {len(boxes)} 个目标")
            
            if len(boxes) > 0:
                print("  详细检测信息:")
                for j, box in enumerate(boxes):
                    cls_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    xyxy = box.xyxy[0].tolist()
                    
                    class_name = model.names[cls_id]
                    print(f"    目标 {j+1}: {class_name}")
                    print(f"      置信度: {conf:.2%}")
                    print(f"      边界框: [{xyxy[0]:.1f}, {xyxy[1]:.1f}, {xyxy[2]:.1f}, {xyxy[3]:.1f}]")
            
            # 检查是否保存了图片
            if hasattr(result, 'save_dir'):
                print(f"  结果图片保存到: {result.save_dir}")
        
        # 6. 额外测试：使用本地图片（如果存在）
        local_test_images = [
            "test.jpg",
            "test.png",
            "data/images/bus.jpg",
            "ultralytics/assets/bus.jpg"
        ]
        
        for img_path in local_test_images:
            if os.path.exists(img_path):
                print(f"\n使用本地图片测试: {img_path}")
                results_local = model.predict(
                    source=img_path,
                    save=True,
                    show=False,
                    conf=0.25,
                    imgsz=640
                )
                print(f"✅ 本地图片测试成功!")
                break
        else:
            print("\nℹ️ 未找到本地测试图片，仅使用了在线图片")
        
        return True
        
    except Exception as e:
        print(f"❌ 推理测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    success = test_yolov8_weights()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 所有测试通过！YOLOv8 环境配置正确。")
        print("\n你可以开始使用以下命令进行训练:")
        print("  python train.py --weights yolov8_pt/yolov8n.pt --data your_data.yaml")
        print("或者:")
        print("  from ultralytics import YOLO")
        print("  model = YOLO('yolov8_pt/yolov8n.pt')")
        print("  model.train(data='your_data.yaml', epochs=100)")
    else:
        print("❌ 测试未通过，请检查上述错误信息。")
    print("=" * 60)

if __name__ == "__main__":
>>>>>>> 02646c286ff348358fce6a3dafefa5a2a2334056
    main()