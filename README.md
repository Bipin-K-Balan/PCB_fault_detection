# PCB_fault_detection




## Problem Statement:
In Electronic Industry PCB (Printed Circuit Board) manufacturing companies are spending too much time and money for Quality Control and Quality Assurance of PCB ensuring that the manufactured PCB is designed as expected and there is no components missing or Short circuits or no design issues. These quality testers are high domain experts and for testing PCB complex boards taking time. So when huge demand arrives from other electronics companies, the client is not able to fullfill their requirement due to the time constraints in Quality checks eventhough they have the capacity to manufacture the demanded units. If they skip Qaulity checks for getting the bulk orders if any design fault in PCB will effect their industrial reputation, if they start to recruit huge domain experts for testing with huge cost for the bulk order time periods, company wont be able to maintain them once the bulk order has completed. So company is looking for a solution which can identify the fault in the manufactured PCB which should be faster than human resources with high accuracy.

## Dataset

<img width="453" alt="DATASET" src="https://user-images.githubusercontent.com/53367536/132630091-d9dbf89c-60fe-4ce3-9b96-556f708806cc.PNG">

We have collected image dataset of PCB by taking video using high resolution (64 MP) camera from the client itself. We considered all angles and different distance to make the detection much more robust. We also used different lighting conditions and shadows as well. Once the video has taken we have take high resolution screenshots of relevant part of the PCB and in various conditions we have collected total 3500 images. These images are later annotated with various components (total 9 classes) in PCB like capacitors, resistors, MOSFETs, transformers in Roboflow plus we have also done Image augmentation by adding some flips, rotations, distortions and noise to make the detection much more accurate in any condition. Roboflow  can transform the images and label file to pytorch format which we used for pytorch YOLOv5 setup. Mov are annotated in YOLO v5 PyTorch and Pascal VOC format as per detection Setup When generating the dataset, we divide 70% into train dataset,15% into validation dataset, and rest into test dataset.

<img width="433" alt="PCB001" src="https://user-images.githubusercontent.com/53367536/132630795-32f77b21-c198-47d1-99d9-f4083ab6f624.PNG"> ![augmentpcb](https://user-images.githubusercontent.com/53367536/132630375-212f74b4-243f-48b2-9c2e-90cc637ed75f.png)

## Training

After several experiements with various models, we have choosed YOLO V5 since its very fast (getting 65 FPS in GPU settings) and providing 95% accuracy on test dataset and another advantage is the model size is very low where it only has 56 MB of size where other model which performing low compared to this having size more than 250 MB. Yolo V5 is came as the pytorch version introduced by Ultralytics pretrained on the COCO dataset. The training took 29 hours in Colab pro with P100 GPU and loss converged below 0.06

## Hyper parameters:
lr0=0.01, lrf=0.2, momentum=0.937, weight_decay=0.0005, warmup_epochs=3.0, warmup_momentum=0.8, warmup_bias_lr=0.1, box=0.05, cls=0.5, cls_pw=1.0, obj=1.0, obj_pw=1.0, iou_t=0.2, anchor_t=4.0, fl_gamma=0.0, hsv_h=0.015, hsv_s=0.7, hsv_v=0.4, degrees=0.0, translate=0.1, scale=0.5, shear=0.0, perspective=0.0, flipud=0.0, fliplr=0.5, mosaic=1.0, mixup=0.0

## Web Integration,UI and Deployment:

<img width="436" alt="webui" src="https://user-images.githubusercontent.com/53367536/132629814-7f6cba29-9f26-4273-ad6f-b6e6fb926a80.PNG">

We have used streamlit for the web ui part which providing amazing user experience than combined HTML and CSS webpages. We have provided variety of options to detect directly from camera device, detect from input video or detect from input image. Since this is a POC project for the client for demo and testing purpose, we have deployed this in GCP, but for production use we are more recommending this to deploy in edge devices like Google Coral or NVIDIA TX2 devices, so that real time prediction and accuracy will be meet the Objectives. Model conversions (converting model file to TFRT or TF lite) are also given.


<img width="463" alt="pcb non defective web ui" src="https://user-images.githubusercontent.com/53367536/132629913-542cdecb-9fc9-41c1-a150-7b856b3e1d71.PNG">


