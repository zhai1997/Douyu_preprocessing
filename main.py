# -*- coding: utf-8 -*-
"""
Created on Tue May  4 20:04:56 2021

@author: IS-group
"""
#%% Import packages
import numpy as np
import pandas as pd
from google.cloud import language_v1
import re
import matplotlib.pyplot as plt
import seaborn as sns
import os
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']

#%% Parameters
#client = language_v1.LanguageServiceClient.from_service_account_json('rapid-will-312108-7875b84f60a5.json')
work_dir= "F:\Reasearch_PHBS"
work_dir+=work_dir[2]


#%% Import data
def read_data(data_kind,names):
    data=[]
    for i in os.listdir(work_dir+data_kind):
        data.append(pd.read_table(work_dir+data_kind+work_dir[2]+i,sep='',header=None,names=names))
    return pd.concat(data)

dt=read_data('dy_tmp_nottingham_school_project_anchor_action_1',
             names=['message_id','user_id','room_id','content','if_fan','color',
                          'if_vip','ct','time'])     
        
dt=dt[dt.message_id.str.len()>30]
dt.time=pd.to_datetime(dt.time)
#%%
streamer=pd.read_table('streamer info.txt',sep='',header=None,
                       names=['room_id','startype_1','startype_2','startype_3','gender','age',
                              'community_id','date_1','date_2','location_1','location2'])
streamer['signup_time']=pd.to_datetime(streamer.date_1.str.cat(streamer.date_2))
star_live=pd.read_table('start_live.txt',sep='',header=None,
                        names=['live_date','room_id','start_time','end_time','roomtype_1','roomtype_2','roomtype_3'])
star_live.start_time=pd.to_datetime(star_live.start_time,unit='s')
star_live.end_time=pd.to_datetime(star_live.end_time,unit='s')

## Define live_id using hash
star_live['live_id']=star_live.room_id.str.cat(star_live.start_time.apply(lambda x:str(x))).apply(hash)
star_live=star_live[star_live.index.isin(star_live.live_id.drop_duplicates().index)]

## Merge tables
dt=dt.merge(streamer[['room_id','startype_1','startype_2','startype_3','signup_time']
        ],how='left',left_on='room_id',right_on='room_id')
#from pandasql import sqldf
#pysqldf = lambda q: sqldf(q, globals())
#dt=pysqldf("""
#        select 
#            live_id
#            message_id,
#            user_id,
#            room_id,
#            content,
#            if_fan,
#            color,
#            if_vip,
#            ct,
#            time,
#            startype_1,
#            startype_2,
#            startype_3,
#            signup_time,
#            start_time,
#            end_time,
#            roomtype_1,
#            roomtype_2,
#            roomtype_3
#        from     
#            dt left join star_live
#            on dt.room_id=star_live.room_id
#            and dt.time>=star_live.start_time
#            and dt.time<=star_live.end_time
#        """)


dt=dt.merge(star_live[['room_id','start_time','end_time','live_id']],
        how='left',left_on='room_id',right_on='room_id')
dt['is_matched']=(dt.time>=dt.start_time)&(dt.time<=dt.end_time)
dt=dt.merge(dt[['message_id','is_matched']].groupby('message_id').is_matched.max(),
         left_on='message_id',right_index=True,how='left',suffixes=('','_any'))
dt.loc[dt[~dt.is_matched_any].index,['start_time','end_time']]=pd.to_datetime(np.nan)
dt.loc[dt[~dt.is_matched_any].index,['live_id']]=np.nan
dt=dt.drop_duplicates()
dt=dt[dt.is_matched|dt.start_time.isna()].drop(['is_matched','is_matched_any'],axis=1)

dt=dt.merge(star_live[['room_id','roomtype_1','roomtype_2','roomtype_3','live_id'
                       ]],left_on='live_id',right_on='live_id',how='left')

## Filter Nonsense
fil=re.compile(r"[^0-9A-Za-z\u4e00-\u9fa5]")#这里留着数字了
dt.content=dt.content.str.replace(fil,'')
dt=dt[dt.content.str.len()>0]

