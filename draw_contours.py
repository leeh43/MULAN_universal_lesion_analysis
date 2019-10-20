#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 10:59:46 2019

@author: leeh43
"""

import os 
import numpy as np
import pandas as pd 
import cv2
import nibabel as nib
import matplotlib.pyplot as plt
from scipy.ndimage.morphology import binary_fill_holes, binary_opening, binary_dilation

def windowing(im, win):
    """scale intensity from win[0]~win[1] to float numbers in 0~255"""
    im1 = im.astype(float)
    im1 -= win[0]
    im1 /= win[1] - win[0]
    im1[im1 > 1] = 1
    im1[im1 < 0] = 0
    im1 *= 255
    return im1

def windowing_rev(im, win):
    """backward windowing"""
    im1 = im.astype(float)/255
    im1 *= win[1] - win[0]
    im1 += win[0]
    return im1

img_num = 'img0001'
input_win = [-1024, 3071]
win_show = [-175, 275]
nifti_zb = os.path.join('/nfs/masi/leeh43/zhoubing100/img/'
                     + img_num + '.nii.gz')
n = nib.load(nifti_zb)
data = n.get_data()
for i in range(data.shape[2]):
    slice_num = i
    c = os.path.join('/nfs/masi/leeh43/MULAN_universal_lesion_analysis/results/_nfs_masi_leeh43_zhoubing100_img_img0001.nii.gz/'
                     + 'slice_' + str(slice_num) + '_mask_c.csv')
    c = pd.read_csv(c)
    c = c['c'].tolist()
    im_scale = c[4] 
    #n = nib.load(nifti_zb)
    #data = n.get_data()
    ############# Ad-hoc change orientation #################
    vol = (n.get_data().astype('int32') + 32768).astype('uint16')  # to be consistent with png files
    # spacing = -data.get_affine()[0,1]
    # slice_intv = -data.get_affine()[2,2]
    aff = n.get_affine()[:3, :3]
    spacing = np.abs(aff[:2, :2]).max()
    slice_intv = np.abs(aff[2, 2])
    
    # TODO: Ad-hoc code for normalizing the orientation of the volume.
    # The aim is to make vol[:,:,i] an supine right-left slice
    # It works for the authors' data, but maybe not suitable for some kinds of nifti files
    if np.abs(aff[0, 0]) > np.abs(aff[0, 1]):
        vol = np.transpose(vol, (1, 0, 2))
        aff = aff[[1, 0, 2], :]
    if np.max(aff[0, :2]) > 0:
        vol = vol[::-1, :, :]
    if np.max(aff[1, :2]) > 0:
        vol = vol[:, ::-1, :]
    
    vol = vol.astype(np.float32,copy=False) - 32768
    data = vol[int(c[0]):int(c[1]) + 1, int(c[2]):int(c[3]) + 1, :]
    data = cv2.resize(data, None, None, fx=im_scale, fy=im_scale, interpolation=cv2.INTER_LINEAR)
    #data = cv2.flip(data, 1 )
    img = np.transpose(data, (2,0,1))
    scale = 2
    #img = (img - img.min())/(img.max()-img.min())
    #img = img*255.0
    #img = np.transpose(data,(2,0,1))
    img = img[slice_num,:,:]
    img = windowing(img, win_show).astype('uint8')
    img = cv2.resize(img, None, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    
    #h, w = img.shape[0], img.shape[1]
    # calculate the center of the image
    #center = (w / 2, h / 2)
    #scale = 1.0 
    #angle90 = 90
    #M = cv2.getRotationMatrix2D(center, angle90, scale)
    #img = cv2.warpAffine(img, M, (h, w)) 
    
    
    data_dir = os.path.join('/nfs/masi/leeh43/MULAN_universal_lesion_analysis/results/')
    file_dir = '_nfs_masi_leeh43_zhoubing100_img_img0001.nii.gz'
    c_l = pd.read_csv(os.path.join(data_dir, file_dir, 'slice_' + str(slice_num) + '_contour_location.csv' ), na_values=' ')
    c_l['list1'].fillna(str(0), inplace=True)
    c_l['list2'].fillna(str(0), inplace=True)
    a = np.zeros((len(c_l), 1, c_l.shape[1]))
    for i in range(c_l.shape[0]):
        x = c_l['list1'][i]
        y = c_l['list2'][i]
        a[i, 0, 0] = float(x)
        a[i, 0, 1] = float(y)
        a = a.round().astype(int)
        if c_l['list1'][i] == 0:
            pass
        
    im_overlay = cv2.drawContours(img, a, -1, (0,255,0), thickness=1)
    save_dir = os.path.join('/nfs/masi/leeh43/zhoubing100/img/' + img_num +'/')
    if os.path.isdir(save_dir) == False:
        os.mkdir(save_dir)
    output_fn = os.path.join(save_dir + '_slice_' + str(slice_num) + '.png')
    cv2.imwrite(output_fn, im_overlay)