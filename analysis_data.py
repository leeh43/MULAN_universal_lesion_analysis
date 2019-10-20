#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 02:29:53 2019

@author: leeh43
"""

import os 
import numpy as np
import json
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import random


def get_files_endswith(src_dir, ext):
    if not os.path.isdir(src_dir):
        raise ValueError('Folder does not exist:' + src_dir)

    file_list = []

    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.lower().endswith(ext.lower()):
                file_list.append(root + '/' + file)
    return file_list

file_list = []
dirs_list = []
data_dir = os.path.join('/nfs/masi/leeh43/MULAN_universal_lesion_analysis/results')
file_list= get_files_endswith(data_dir, '.txt')

data_list = []
for i in file_list:
    with open(i) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    data_list.append(content)

json_file = os.path.join('/nfs/masi/leeh43/MULAN_universal_lesion_analysis/program_data/'
                         + 'tags_cache.json')
with open(json_file) as f:
    json_data = json.load(f)
tag_class=[]
tag_class = json_data['tag_dict_list']
tag_list = []
tag = []
for item in tag_class:
    tag_list.append(item['tag'])
    
################## Get Tag List Completed ######################
intermediate_list = []
num_list = []
for tag in tag_list:
    for item in data_list:
        for row in item:
            if tag in row:
                intermediate_list.append(row)
    num_list.append(len(intermediate_list))
    intermediate_list = []
    
################ Plot Graph ###################
#width = 0.5
#fig = plt.figure(figsize=(10,40))
#y_pos = np.arange(len(tag_list))
#plt.barh(y_pos,num_list, width, align='center')
#plt.yticks(y_pos, tag_list)
#plt.xlabel('Numbers in Zhoubing datasets')
#plt.title('Evaluation of DeepLesion on Zhoubing100')

#plt.show()                
#fig.set_size_inches(25, 40)
#fig.savefig('evaluation.png', dpi=300)
    
################# Total number of lesion ################
num_lesion = []
for item in data_list:
    for row in item:
        if 'lesion' in row:
            num_lesion.append(row)

################# Total number of liver lesion ################
liver_list = []
for item in num_lesion:
    if 'liver' in item:
        liver_list.append(item)
