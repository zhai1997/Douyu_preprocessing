# -*- coding: utf-8 -*-
"""
Created on Wed May  5 15:57:32 2021

@author: IS-group
"""
#%% define functions
import os 
import re

work_dir= "F:\Reasearch_PHBS"
work_dir+=work_dir[2]

def read_data(data_kind,table_name):
    for i in os.listdir(work_dir+data_kind):
        #if int(i[:6])<909:continue
        focal_file=work_dir+data_kind+work_dir[2]+i
        focal_file=re.sub(r'\\',r'\\\\',focal_file)
        command=("mysql -e \"load data local infile '" + focal_file + "' ignore into table douyu." +
                 table_name+ " fields terminated by ','\" -u root --password=root --local-infile=1")
        print('running:  '+command)
        back=os.system(command)
        #print('back:  '+str(back))
  
#%% import data
read_data('start_live','start_live')
read_data('dy_tmp_nottingham_school_project_anchor_info_1','streamer')
