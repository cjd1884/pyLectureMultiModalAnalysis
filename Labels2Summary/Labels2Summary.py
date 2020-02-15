#!/usr/bin/env python
# coding: utf-8

# # pyLectureMultiModalAnalysis
# 
# ## Summary of video segments
# 
# ### Functions: 4
# #### add_duration(), labels2summary(),summary2video(),df2summary()
# 
# ### Author: Stelios Karozis

# In[438]:


#import pandas as pd
#import numpy as np

#df=pd.read_csv('../data/index.csv', sep=';')
#df


# In[439]:


def add_duration(df, folder='../data/'):
    from pymediainfo import MediaInfo
    dur=[]
    for index,f in df.iterrows():
        #print(f['FILE'])
        media_info = MediaInfo.parse(folder+f['FILE']+'/'+f['SEG']+'.mp4')
    #duration in milliseconds
        duration_in_s = media_info.tracks[0].duration/1000
        dur.append(duration_in_s)
    df['DURATION']=dur
    return df


# In[440]:


#add_duration(df=df)


# In[487]:


def labels2summary(df, col_cl='CLASS_1', label=['boring','interesting','neutral'], prc_l=[0.30,0.35,0.35], col_d='DURATION', duration_sec=90):
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


def summary2video(df, output_folder='../data/', output_name='summary.mp4'):
    import os
    from pymediainfo import MediaInfo
    from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip
    
    try:
        os.remove(output_name)
    except OSError:
        pass
    clips=[]
    for i, new_df in df.groupby(level=0):
        for folder,file in df.loc[i].iterrows():
            print(folder,file['SEG'])
            clip = VideoFileClip(output_folder+folder+'/'+file['SEG']+'.mp4')
            clips.append(clip)
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_folder+output_name)
    
    media_info = MediaInfo.parse(output_folder+output_name)
    duration_in_s = media_info.tracks[0].duration/1000
    print('Summary duration is:', duration_in_s)


# In[486]:


#summary2video(df=summary)


# In[ ]:

def df2summary(df, folderDATA='../data/' ,col_cl='CLASS_1', label=['boring','interesting','neutral'], prc_l=[0.30,0.35,0.35], col_d='DURATION', duration_sec=90, output_folder= '../data/', output_name='summary.mp4'):

    df_dur=add_duration(df=df, folder=folderDATA)

    summary=labels2summary(df=df_dur, col_cl=col_cl, label=label, prc_l=prc_l, col_d=col_d, duration_sec=duration_sec)

    summary2video(df=summary, output_folder=output_folder, output_name=output_name)
    
    return print('Enjoy your summary video !')

