# -*- coding: utf-8 -*-
"""
Created on Sat May 15 17:38:03 2021

@author: IS-group
"""

import numpy as np
import pandas as pd
import os
from os.path import join, getsize
import re
import csv
import sys


focal_dir='F:\Reasearch_PHBS\dy_tmp_nottingham_school_project_send_msg_2'
#focal_dir='F:\Reasearch_PHBS\danmu_debug'
out_put=0
counter=1
# left=pd.to_datetime('2019-10-01')
# right=pd.to_datetime('2019-12-31')
output_folder='danmu_new_debug'
time_range=pd.PeriodIndex(np.random.choice(pd.date_range(start='2019-10-01',end='2019-11-30'),7),freq='d')
emoji_pat=re.compile(u'[\U00010000-\U0010ffff]')
log_file=output_folder+'.log'

try:
    os.mkdir('logs')
except:
    pass

log_f=open(join('logs',log_file), 'w')
def my_print(*x):
    [print(*x,file=i) for i in [sys.stdout,log_f]]
    
def my_filter(ser):
    chunk=ser.copy()
    chunk=chunk[pd.notnull(chunk.content)]
    chunk.time=pd.to_datetime(chunk.time)
    #chunk=chunk[pd.PeriodIndex(chunk.time,freq='d').isin(time_range)]
    chunk.content=chunk.content.str.replace(emoji_pat,'')
    return chunk

def write_to_file(chunk,counter,output_file):
    chunk.to_csv(output_file, mode='a',header=False,index = None)
    #print('fininsh Chunk',counter)
    
try:
    os.mkdir(output_folder)
except:
    pass


for i in os.listdir(focal_dir):
    #if int(i[:6])!=23: continue
    train_data = pd.read_table(join(focal_dir,i),iterator=True,header=None,sep='',
                               names=['message_id','user_id','room_id','content','if_fan','color',
                          'if_vip','ct','time'],lineterminator='\n',quoting=csv.QUOTE_NONE)
   
    my_print(join(focal_dir,i))  
    ##生成chunk，读chunk
    while True:    
        output_file=join('F:\Reasearch_PHBS',output_folder,str(out_put)+'.csv')#Decide the file to write
        try: 
            if getsize(output_file)> 3425126780: out_put+=1
        except:
            pass
        
        try:
            
            chunk = train_data.get_chunk(56000).drop(['message_id','color','ct'],axis=1) 
            chunk=my_filter(chunk)    
        except Exception as e: 
            if str(e)=='':##如果错误是读完了
                write_to_file(chunk,counter,output_file)              
                counter+=1
                break##then we will continue to the next file
            my_print(e,' at the bunch attempt')##if it is other errors, we will consider reading by rows
           
            chunk_mod=pd.DataFrame(columns=chunk.columns)#In this way, we can garantee that rows with error will be ignored
            for j in range(chunk.shape[0]):               
                try:
                    chunk_mod=chunk_mod.append(my_filter(chunk.iloc[[j],:]).iloc[0,:])
                except Exception as e1:
                    if str(e1)!='single positional indexer is out-of-bounds': # if the error is no remaining row, ignore
                        my_print('        ', j, ' find the error',str(e1))   # Otherwise, print the error
                    pass# for both situations, we will skip that row
            write_to_file(chunk_mod,counter,output_file) ## After we get the resuls by row by row method, we write it into the file              
            counter+=1
            continue##and continue to the next chunk
        write_to_file(chunk,counter,output_file)#if there is not error in one chunk, we write it into the file and continue to the next chunk
        counter+=1
log_f.close()

