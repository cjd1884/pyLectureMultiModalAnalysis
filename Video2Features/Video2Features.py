#!/usr/bin/env python
# coding: utf-8

# # pyLectureMultiModalAnalysis
# 
# ## Feature extraction from video segment
# 
# ### Functions: 3
# #### RandomVector(), video2frame(), frame2features()
# 
# ### Author: Stelios Karozis

# ## RandomVector()

# In[51]:


def RandomVector(trainmode=True,sz=100):
    import pickle
    import numpy as np
    from numpy import array
    import random
    
    if trainmode==False:
        try:
            vector = pickle.load(open("random.pickle", "rb"))
        except (OSError, IOError) as e:
            vector = 3
            print('Error the random vector is missing')
    else:
        vector=[]
        for i in range(sz):
            tmp=random.uniform(0.5, 1.0)
            vector.append(tmp)
    with open('random.pickle','wb') as f:
        pickle.dump(array(vector), f)
    return array(vector)


# ## video2frame()

# In[30]:


def video2frame(count,sec,folderVID,file,folderIMG):
    import cv2
    vidcap = cv2.VideoCapture(folderVID+file)
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
        cv2.imwrite(folderIMG+str(count)+".jpg", image)     # save frame as JPG file
    return hasFrames,folderIMG+str(count)+".jpg"   #folderIMG+file+'_'+str(count)+".jpg"


# ### test

# In[ ]:


# file='hd0456.mov'
# sec = 0
# frameRate = 0.5 #//it will capture image in each 0.5 second -> 2fps
# count=1
# success,a = video2frame(sec,'./',file,'./')
# while success:
    # count = count + 1
    # sec = sec + frameRate
    # sec = round(sec, 2)
    # success,a = video2frame(sec,'./',file,'./')


# ## frame2features

# In[81]:


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
    tf.reset_default_graph()
    vector = RandomVector(trainmode=True,sz=100)
    return np.dot(feature[:,None],vector[None,:])


# ### test

# In[ ]:


#frame2features('1.jpg')


# ## Video2feature()

# In[83]:


def Video2feature(pathIn='./data/',frameRate=0.5, save=True):
    import os
    import glob
    import numpy as np
    import pandas as pd
    import pathlib
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    pathIn=pathIn
    index = pd.read_csv(pathIn+'index.csv', sep=';')

    frameRate = frameRate #//it will capture image in each 0.5 second -> 2fps
    ftr_array=[]

    for f,s in index[['FILE','SEG']].values:
      
        pathOut=pathIn+f+'/frames/'
        if not os.path.exists(pathOut):
            os.makedirs(pathOut)
     
        files=f+'/'+str(s)   
        files=glob.glob(pathIn+files+'*')[0]
        suffix=os.path.splitext(files)[1]
        files=f+'/'+str(s)+suffix
        ftr_fr=[]
        filename=pathIn + files
        print(filename)
        sec = 0
        count=1
        success,fr = video2frame(count,sec,pathIn,files,pathOut)
        print(fr)
        ftr = frame2features(fr)
        ftr_fr.append(ftr)

        while success:
            count = count + 1
            sec = sec + frameRate
            sec = round(sec, 2)
            success,fr = video2frame(count,sec,pathIn,files,pathOut)
            if success == True:
                print(fr)
                ftr = frame2features(fr)
                ftr_fr.append(ftr)
        ftr_fr = np.vstack(ftr_fr) 
        ftr_fr = np.average(ftr_fr, axis=0)
        ftr_array.append(ftr_fr)
        
    ftr_array = np.vstack(ftr_array)


    ftr_df = pd.DataFrame(data=ftr_array)
    df=index.copy()
    df=pd.concat([df,ftr_df], axis=1)

    if save == True:
        df.to_pickle(pathIn+'Video2Features.pkl')

    return df


# In[85]:


#df = Video2feature(pathIn='../data/',frameRate=0.5, save=False)
#df


# In[33]:





# In[ ]:




