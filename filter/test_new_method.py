# -*- coding: utf-8 -*-
"""
Created on Thu May 13 00:20:47 2021

@author: IS-group
"""

import pandas as pd
import os
from os.path import join, getsize

focal_dir='F:\Reasearch_PHBS\dy_tmp_nottingham_school_project_start_live'
out_put=0
for i in os.listdir(focal_dir):
    train_data = pd.read_table(join(focal_dir,i),iterator=True,header=None,sep='',
                               names=['live_date','room_id','start_time','end_time','roomtype_1','roomtype_2','roomtype_3'])
    print(join(focal_dir,i))
    while True:
        try:
            chunk = train_data.get_chunk(5600000)
            output_file=join('F:\Reasearch_PHBS\start_live',str(out_put)+'.csv')
            chunk.to_csv(output_file, mode='a',header=False,index = None)
            if getsize(output_file)> 3425126780: i+=1
        except Exception as e: 
            break
        
    
