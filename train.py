# -*- coding: utf-8 -*-
from ultralytics import YOLO
import os
classes = {0:'单车' ,1:'卡车', 2:'摩托车', 3:'汽车'}
# 加载模型
model = YOLO('yolov8n.pt')# 加载预训练模型
#训练模型
results = model.train(data='car.yaml', epochs=100)

# 导出模型
# model.export(format='openvino')
img = "./data/tests/5.jpg"
name = img.split('/')[-1].split('.')[0]
# 模型预测
model = YOLO('./runs/detect/train2/weights/best.pt')
num = len(os.listdir('runs/detect'))-2
model.predict(source=img, save=True, save_txt=True, conf=0.4)
with open(f'runs/detect/predict{num}/labels/{name}.txt','r') as f:
    a = int(f.read().split(' ')[0])
    print(classes[a])
    f.close()

'''
可在终端直接训练
yolo task=detect    mode=train    model=yolov8n.pt        args...
          classify       predict        yolov8n-cls.yaml  args...
          segment        val            yolov8n-seg.yaml  args...
                         export         yolov8n.pt        format=onnx  args...
单卡训练：
yolo task=detect mode=train model=yolov8n.pt data=data/car.yaml batch=32 epochs=100 workers=16 device=0
多卡训练：
yolo task=detect mode=train model=yolov8n.pt data=data/car.yaml batch=32 epochs=100 workers=16 device=\'0,1,2,3\'
模型验证：
yolo task=detect mode=val model=runs/detect/train3/weights/best.pt data=data/car.yaml device=0 plots=True
模型预测：
yolo task=detect mode=predict model=runs/detect/train3/weights/best.pt source=data/images device=0
模型导出：
yolo task=detect mode=export model=runs/detect/train3/weights/best.pt format=onnx
'''