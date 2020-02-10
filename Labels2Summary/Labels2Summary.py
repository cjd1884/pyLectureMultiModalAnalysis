#!/usr/bin/env python
# coding: utf-8

# # pyLectureMultiModalAnalysis
# 
# ## Summary of video segments
# 
# ### Functions: 3
# #### add_duration(), labels2summary(),summary2video()
# 
# ### Author: Stelios Karozis

# In[438]:


#import pandas as pd
#import numpy as np

#df=pd.read_csv('../data/index.csv', sep=';')
#df


# In[439]:


def add_duration(df=df):
    from pymediainfo import MediaInfo
    dur=[]
    for index,f in df.iterrows():
        #print(f['FILE'])
        media_info = MediaInfo.parse('../data/'+f['FILE']+'/'+f['SEG']+'.mp4')
    #duration in milliseconds
        duration_in_s = media_info.tracks[0].duration/1000
        dur.append(duration_in_s)
    df['DURATION']=dur
    return df


# In[440]:


#add_duration(df=df)


# In[487]:


def labels2summary(df=df, col_cl='CLASS_1', label=['boring','interesting','neutral'], prc_l=[0.30,0.35,0.35], col_d='DURATION', duration_sec=90):
    summary={}
    i=0
    for l,p in zip(label, prc_l):
        df_label=df.loc[df[col_cl] == l]
        
        #In order to meet the total duration of summary we use the avg duration of each class
        avg_dur=round(df_label[col_d].mean())
        
        #We calculate the seconds correspond to each class
        #and then how many parts of each class (of avg duration) 
        #need to be used for each time span 
        if duration_sec != -1:
            ndx=int(round((p*duration_sec/avg_dur)))
        else:
            ndx=int(len(df_label[col_cl])*p)
            
        tmp=df_label[['FILE','SEG',col_cl]].iloc[0:ndx]

        i=i+1
        if i == 1:
            summary=tmp
        else:
            summary=pd.concat([summary,tmp])
    return summary.reset_index().set_index([col_cl,'FILE'])


# In[462]:


#summary= labels2summary(df=df, col_cl='CLASS_1', label=['boring','interesting','neutral'], prc_l=[0.30,0.35,0.35], col_d='DURATION', duration_sec=360)
#summary


# In[485]:


def summary2video(df=summary, output='summary.mp4'):
    import os
    from pymediainfo import MediaInfo
    from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip
    
    try:
        os.remove(output)
    except OSError:
        pass
    clips=[]
    for i, new_df in df.groupby(level=0):
        for folder,file in df.loc[i].iterrows():
            print(folder,file['SEG'])
            clip = VideoFileClip('../data/'+folder+'/'+file['SEG']+'.mp4')
            clips.append(clip)
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile('../data/'+output)
    
    media_info = MediaInfo.parse('../data/'+output)
    duration_in_s = media_info.tracks[0].duration/1000
    print('Summary duration is:', duration_in_s)


# In[486]:


#summary2video(df=summary)


# In[ ]:




