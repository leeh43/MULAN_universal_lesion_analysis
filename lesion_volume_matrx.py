#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 14:28:12 2019

@author: leeh43
"""

import os 
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

n_data = 'zhoubing100'
num_list = []
lesion_volume = []
mean_confid_list = []
num_lesion_list = []
for num in range(100):
    if num + 1  < 10:       
        img_num = 'img000' + str(num + 1)
        data_dir = '/nfs/masi/leeh43/MULAN_universal_lesion_analysis/results'
        img_dir = '_nfs_masi_leeh43_zhoubing100_img_' + img_num + '.nii.gz/'
        result = os.path.join(data_dir, img_dir + 'results.txt' )
        main_dir = '/nfs/masi/leeh43/zhoubing100/img/'
        mask_dir = os.path.join(main_dir, img_num, 'contour_mask.nii.gz')
        
    if num + 1 >= 10 and num + 1 < 100:       
        img_num = 'img00' + str(num + 1)
        data_dir = '/nfs/masi/leeh43/MULAN_universal_lesion_analysis/results'
        img_dir = '_nfs_masi_leeh43_zhoubing100_img_' + img_num + '.nii.gz/'
        result = os.path.join(data_dir, img_dir + 'results.txt' )
        main_dir = '/nfs/masi/leeh43/zhoubing100/img/'
        mask_dir = os.path.join(main_dir, img_num, 'contour_mask.nii.gz')
        
    if num + 1 == 100:       
        img_num = 'img0' + str(num + 1)
        data_dir = '/nfs/masi/leeh43/MULAN_universal_lesion_analysis/results'
        img_dir = '_nfs_masi_leeh43_zhoubing100_img_' + img_num + '.nii.gz/'
        result = os.path.join(data_dir, img_dir + 'results.txt' )
        main_dir = '/nfs/masi/leeh43/zhoubing100/img/'
        mask_dir = os.path.join(main_dir, img_num, 'contour_mask.nii.gz')
    
    print('Zhoubing Dataset Number: %.d' % (num+1))
    
    num_list.append((num+1))


    n = 0;
    mask = nib.load(mask_dir)
    mask_n = mask.get_data()
    r_n = mask.header.get_zooms()
    d_x, d_y, d_z = r_n[0], r_n[1], r_n[2]
    for z in range(mask_n.shape[2]):
        for j in range(mask_n.shape[1]):
            for i in range(mask_n.shape[0]):
                if int(mask_n[i,j,z]) != 0:
                    n = n + 1
                else:
                    pass
    
    data_dir = '/nfs/masi/leeh43/MULAN_universal_lesion_analysis/results'
    img_dir = '_nfs_masi_leeh43_zhoubing100_img_' + img_num + '.nii.gz/'
    result = os.path.join(data_dir, img_dir + 'results.txt' )
    #print('Zhoubing Dataset Number: %.d' % (num+1))
        
    with open(result) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    liver_list = []
    
    list_nspace = []
    final_list = []
    for item in content:
        if item != '':
            list_nspace.append(item)
    for item in list_nspace:
        if 'slice' not in item:
            final_list.append(item)
    for i in range(len(content)):
        if 'liver' in content[i]:
            row = content[i].split('score: ')[1]
            score = row.split('|')[0]
            #print(score)
            liver_list.append(float(score))
            
    if liver_list != []:
        mean_confid = sum(liver_list) / len(liver_list)
        print('Mean confidence level is: %.4f' % mean_confid)
    
    #final_list.append('Dataset ' + str(num+1))
    mean_confid_list.append(mean_confid)
    
    print('Number of Slice with Liver Lesion: %d' % len(liver_list))
    num_lesion_list.append(len(liver_list))
    
    Voxl_liver_lesion = n * (len(liver_list) / len(final_list)) * (d_x*d_y*d_z)
    lesion_volume.append(Voxl_liver_lesion)
    print('Lesion Volume: %.8f' % Voxl_liver_lesion)

    
    # Write result to .txt files
    txt_dir = os.path.join(main_dir, 'lesion_volume_analysis')
    if os.path.isdir(txt_dir) == False:
        os.mkdir(txt_dir)
    log_f = os.path.join(txt_dir, n_data + '_volume_analysis.txt')
    fv = open(log_f, 'a')
    fv.write('Zhoubing Dataset Number: %.d \nNumber of Slice with Liver Lesion: %d \nLesion Volume: %.4f\n'
             % ((num+1), len(liver_list), Voxl_liver_lesion))
    
fv.close()

lesion_volume_rescale = []
for item in lesion_volume:
    a = int(item) / 10000
    lesion_volume_rescale.append(a)

plt.figure(1)
plt.scatter(mean_confid_list,lesion_volume_rescale)
plt.ylabel('Lesion Volume Metric (x10000) (mm^3)')
plt.xlabel('Mean Confidence Level')
plt.savefig('LesionVolume_versus_Mean_Confid_lv.png', dpi=500)

plt.figure(2)
plt.bar(num_list,lesion_volume_rescale)
plt.ylabel('Lesion Volume Metric (x10000) (mm^3)')
plt.xlabel('Zhoubing Datasets Subjects')
plt.savefig('LesionVolume_versus_Subjects.png', dpi=500)

plt.figure(3)
plt.bar(num_list, num_lesion_list)
plt.ylabel('Number of Lesions')
plt.xlabel('Zhoubing Datasets Subjects')
plt.savefig('NumberLesion_versus_Subjects.png', dpi=500)
plt.show()


    
