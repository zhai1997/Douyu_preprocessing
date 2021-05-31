#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 29 20:00:56 2021

@author: mrzhai
"""
#%% import packages and set parameters


import pandas as pd
import numpy as np
from google.cloud import language_v1
client = language_v1.LanguageServiceClient.from_service_account_json('rapid-will-312108-7875b84f60a5.json')



#%% import data
newt=pd.read_table('20191214.csv',sep='\t',header=None, names=['live_id',
'room_id',
'user_id',
'content',
'if_fan',
'if_vip',
'time',
'startype_1',
'startype_2',
'startype_3',
'gender',
'age',
'community_id',
'sign_date',
'location_1',
'location_2',
'start_time',
'end_time',
'follower_num_2017',
'follower_num_2018',
'follower_num_2019'])

newt['start_time']=pd.to_datetime(newt['start_time'])
newt['end_time']=pd.to_datetime(newt['end_time'])
newt.time=pd.to_datetime(newt.time)

newt=newt[newt['end_time']<'2020-12-31'].drop_duplicates()
#newt.groupby([1,16,17])[0].count().to_excel('14.xlsx')

#%% group data
newt['group']=(newt.time-newt.start_time).apply(lambda x:round(x.total_seconds()/60/10))
newt.content=newt.content.astype(str)

gred=newt.groupby(['live_id',
'room_id',
'user_id',
'if_fan',
'if_vip',
'startype_1',
'startype_2',
'startype_3',
'gender',
'age',
'community_id',
'sign_date',
'location_1',
'location_2',
'start_time',
'end_time',
'follower_num_2017',
'follower_num_2018',
'follower_num_2019',
'group']).agg(
    content=('content',lambda x: ' '.join(x))).reset_index()


#%% Get Sentiment
def get_sentiment(text):
    document=language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment=client.analyze_sentiment(request={'document': document}).document_sentiment
    return sentiment.score, sentiment.magnitude

gred['score']=np.nan
gred['manitude']=np.nan
for i in gred.index:
    if i%1000==0: print(i)
    gred.loc[i,'score'], gred.loc[i,'magnitude']=get_sentiment(gred.loc[i,'content'])
