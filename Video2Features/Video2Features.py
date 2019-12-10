#!/usr/bin/env python
# coding: utf-8

# # pyLectureMultiModalAnalysis
#
# ## Feature extraction from video segment
#
# ### Functions: 2
# #### video2frame(), frame2features()
#
# ### Author: Stelios Karozis

# ## video2frame()

# In[1]:


def video2frame(sec,folderVID,file,folderIMG):
    import cv2
    vidcap = cv2.VideoCapture(folderVID+file)
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
        cv2.imwrite(folderIMG+file+'_'+str(count)+".jpg", image)     # save frame as JPG file
    return hasFrames,folderIMG+file+'_'+str(count)+".jpg"


# ## frame2features

# In[2]:


def frame2features(frame):
    import tensorflow as tf
    from keras.preprocessing import image
    from keras.applications.vgg16 import VGG16
    from keras.applications.vgg16 import preprocess_input
    import numpy as np

    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(config=config)

    model = VGG16(weights='imagenet', include_top=False)
    #model.summary()

    fr_path = frame
    fr = image.load_img(fr_path, target_size=(224, 224))
    fr_data = image.img_to_array(fr)
    fr_data = np.expand_dims(fr_data, axis=0)
    fr_data = preprocess_input(fr_data)

    vgg16_feature = model.predict(fr_data)

    vgg16_feature_np = np.array(vgg16_feature)
    feature = vgg16_feature_np.flatten()
    return feature


# ## Combined

# In[3]:


import os
from os.path import isfile, join
import numpy as np
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
pathIn= './videos/'
pathOut='./frames/'


frameRate = 0.5 #//it will capture image in each 0.5 second -> 2fps
ftr_array=[]
files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]#for sorting the file names properly
files.sort(key = lambda x: x[5:-4])
for i in range(len(files)):
    ftr_fr=[]
    filename=pathIn + files[i]
    print(filename)
    sec = 0
    count=1
    success,fr = video2frame(sec,pathIn,files[i],pathOut)
    ftr = frame2features(fr)
    ftr_fr.append(ftr)

    while success:
        count = count + 1
        sec = sec + frameRate
        sec = round(sec, 2)
        success,fr = video2frame(sec,pathIn,files[i],pathOut)
        if success == True:
            print(fr)
            ftr = frame2features(fr)
            ftr_fr.append(ftr)
    ftr_fr = np.vstack(ftr_fr) 
    ftr_fr = np.average(ftr_fr, axis=0)
    ftr_array.append(ftr_fr)
ftr_array = np.vstack(ftr_array)

np.save('Video2Features',ftr_array)
# In[4]:

print(ftr_array.shape)

# In[ ]:
