# -*- coding: utf-8 -*-
"""
Created on Thu May 13 01:34:24 2021

@author: IS-group
"""


import pandas as pd
import os
from os.path import join, getsize
import time
from datetime import datetime

to_unixtime=lambda x: time.mktime(datetime.fromisoformat(x).timetuple())
left=to_unixtime('2019-01-01')
right=to_unixtime('2019-12-31')


focal_dir='F:\Reasearch_PHBS\dy_tmp_nottingham_school_project_start_live'
out_put=0
for i in os.listdir(focal_dir):
    train_data = pd.read_table(join(focal_dir,i),iterator=True,header=None,sep='',
                               names=['live_date','room_id','start_time','end_time','roomtype_1','roomtype_2','roomtype_3'])
    print(join(focal_dir,i))
    while True:
        try:
            chunk = train_data.get_chunk(560000).drop(['roomtype_1','roomtype_2','roomtype_3'],axis=1)
            chunk=chunk[(chunk.start_time>=left)&(chunk.start_time<=right)]
            output_file=join('F:\Reasearch_PHBS\start_live_debug','2019_'+str(out_put)+'.csv')
            chunk.to_csv(output_file, mode='a',header=False,index = None)
            if getsize(output_file)> 34251267800: out_put+=1
        except Exception as e: 
            print(e)
            break
        
    
