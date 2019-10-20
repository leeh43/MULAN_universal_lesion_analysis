#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 10:53:04 2019

@author: leeh43
"""

import os 
import pandas as pd
import numpy as np
import nibabel as nib
import cv2

### Get Slice with liver only ###
result_dir = os.path.join('/nfs/masi/leeh43/MULAN_universal_lesion_analysis/results/_nfs_masi_leeh43_zhoubing100_img_img0001.nii.gz/')
with open(result_dir + 'results.txt') as f:
    content = f.readlines()
content = [x.strip() for x in content]
content = str(content).split('/n')
liver_list = []
for item in content:
    if item == 'liver':
        liver_list.append(slices if slices in content[i] for i in range(len(content)))
#for item in content

### load all contours ###
png_num = []
for png_img in os.listdir(result_dir):
    if png_img.endswith('.png'):
        png_num.append(png_img)

coord_list_1 = []   
coord_list_2 = [] 
for item in os.listdir(result_dir):
    if item.endswith('contour_location.csv'):
        for i in range(len(png_num)):
            df = pd.read_csv(result_dir + 'slice_' + str(i) + '_contour_location.csv', na_values=' ')
            df['list1'].fillna(int(0), inplace=True)
            list_1 = df['list1'].tolist()
            df['list2'].fillna(int(0), inplace=True)
            list_2 = df['list2'].tolist()
            coord_list_1.append(list_1)
            coord_list_2.append(list_2)

for item in coord_list_1:
    if len(item) == 0:
        coord_list_1.remove(item)
        
for item in coord_list_2:
    if len(item) == 0:
        coord_list_2.remove(item)

size = 0
for i in range(len(coord_list_1)):
        size += len(coord_list_1[i])

count_x = 0
a = np.zeros((size, 1, 2))
for contour_x in coord_list_1:
    for num_x in contour_x:
        a[count_x, 0, 0] = num_x
        count_x = count_x + 1
        
count_y = 0
for contour_y in coord_list_2:
    for num_y in contour_y:
        a[count_y, 0, 1] = num_y
        count_y = count_y + 1

a = a.round().astype(int)