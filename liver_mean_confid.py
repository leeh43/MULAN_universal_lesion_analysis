#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 14:48:01 2019

@author: leeh43
"""

import os 
import numpy as np
import matplotlib.pyplot as plt

final_list = []
for num in range(100):
    if num + 1  < 10:       
        img_num = 'img000' + str(num + 1)
        data_dir = '/nfs/masi/leeh43/MULAN_universal_lesion_analysis/results'
        img_dir = '_nfs_masi_leeh43_zhoubing100_img_' + img_num + '.nii.gz/'
        result = os.path.join(data_dir, img_dir + 'results.txt' )
    if num + 1 > 10 and num + 1 < 100:       
        img_num = 'img00' + str(num + 1)
        data_dir = '/nfs/masi/leeh43/MULAN_universal_lesion_analysis/results'
        img_dir = '_nfs_masi_leeh43_zhoubing100_img_' + img_num + '.nii.gz/'
        result = os.path.join(data_dir, img_dir + 'results.txt' )
    if num + 1 == 100:       
        img_num = 'img0' + str(num + 1)
        data_dir = '/nfs/masi/leeh43/MULAN_universal_lesion_analysis/results'
        img_dir = '_nfs_masi_leeh43_zhoubing100_img_' + img_num + '.nii.gz/'
        result = os.path.join(data_dir, img_dir + 'results.txt' )
    
    print('Zhoubing Dataset Number: %.d' % (num+1))
    
    with open(result) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    liver_list = []
    
    for item in content:
        if item == '':
            content.remove(item)
    
    for i in range(len(content)):
        if 'slice' in content[i]:
            print(content[i])
        if 'liver' in content[i]:
            row = content[i].split('score: ')[1]
            score = row.split('|')[0]
            print(score)
            liver_list.append(float(score))        
    
    if liver_list != []:
        mean_confid = sum(liver_list) / len(liver_list)
        print('Mean confidence level is: %.4f' % mean_confid)
        
    #final_list.append('Dataset ' + str(num+1))
    final_list.append(mean_confid)
x = list(range(1, 16))
y = [9, 6, 12, 3, 10, 11, 6, 5, 15, 11, 22, 11, 9 ,19, 16]
plt.figure(1)
plt.scatter(final_list[:15],y)
plt.ylabel('Lesion Volume')
plt.xlabel('Mean Confidence Level')
plt.savefig('LesionVolume_versus_Mean_Confid_lv.png', dpi=500)

plt.figure(2)
plt.bar(x,y)
plt.ylabel('Lesion Volume')
plt.xlabel('Zhoubing datasets subjects')
plt.savefig('LesionVolume_versus_Subjects.png', dpi=500)
plt.show()
