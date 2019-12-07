# Video to Frames to Features
The current directory consist of 2 functions:
1. converts a video to images, using a user defined fps
2. reads the images and creates features using the VGG16 pretrained model 
# module in use
1. import cv2
2. from keras.preprocessing import image
3. from keras.applications.vgg16 import VGG16
4. from keras.applications.vgg16 import preprocess_input
5. import numpy
6. import os
