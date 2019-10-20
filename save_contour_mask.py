#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 12:48:02 2019

@author: leeh43
"""

import os 
import numpy as np
import pandas as pd 
import cv2
import nibabel as nib
import matplotlib.pyplot as plt
from scipy.ndimage.morphology import binary_fill_holes, binary_opening, binary_dilation

def padding(img,bestSize):
    #nimg = img.get_fdata()
    nimg = img
#     print(nimg.size())
    
    padImg = np.zeros(bestSize)
    padImgCenter = np.array([x/2 - 1 for x in bestSize]).astype(np.int32)
    originImgCenter = []
    for x in nimg.shape:
        if (x % 2):
            originImgCenter.append(x/2-1)
        else:
            originImgCenter.append((x+1)/2-1)
    originImgCenter = np.array(originImgCenter).astype(np.int32)

    shift = padImgCenter - originImgCenter
    #padImg[shift[0]:shift[0]+nimg.shape[0],shift[1]:shift[1]+nimg.shape[1],shift[2]:shift[2]+nimg.shape[2]]\
    #= nimg[:,:,:]
    
    ### 2D ###
    padImg[shift[0]:shift[0]+nimg.shape[0],shift[1]:shift[1]+nimg.shape[1]] = nimg[:,:]
    
#     resizeImg = transform.resize(padImg,[256,256,32])  
    
#     print(resizeImg.shape)
    
    #NiftyPadImg = nib.Nifti1Image(padImg,affine = img.affine)
    
    return padImg

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

img_num = 'img0003'
input_win = [-1024, 3071]
win_show = [-175, 275]
nifti_zb = os.path.join('/nfs/masi/leeh43/zhoubing100/img/'
                     + img_num + '.nii.gz')
n = nib.load(nifti_zb)
data_ori = n.get_data()
data = n.get_data()
#new_img = np.zeros((1000, 1000, data.shape[2]))
final_mask = np.zeros((512, 512, data.shape[2]))
for i in range(data.shape[2]):
    slice_num = i
    print('Slice Number = %d' % slice_num)
    c = os.path.join('/nfs/masi/leeh43/MULAN_universal_lesion_analysis/results/_nfs_masi_leeh43_zhoubing100_img_'+ str(img_num) + '.nii.gz/'
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
    aff_1 = aff
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
    data_1 = data
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
    
    mask = np.zeros_like(img)
    data_dir = os.path.join('/nfs/masi/leeh43/MULAN_universal_lesion_analysis/results/')
    file_dir = '_nfs_masi_leeh43_zhoubing100_img_'+ str(img_num) + '.nii.gz'
    c_l = pd.read_csv(os.path.join(data_dir, file_dir, 'slice_' + str(slice_num) + '_contour_location.csv' ), na_values=' ')
    #c_l.dropna()
    #print(c_l.iloc[57,:])
    #c_l['list1'].fillna(str(0), inplace=True)
    #c_l['list2'].fillna(str(0), inplace=True)
    
    count = 0
    # = np.zeros((len(c_l), 1, c_l.shape[1]))
    contour_list = []
    a = []
    for num in range(c_l.shape[0]):
        if (np.isnan(c_l['list1'][num])):
            contour_list.append(a)
            a = []
        if (not np.isnan(c_l['list1'][num])):
            x = c_l['list1'][num]
            y = c_l['list2'][num]
            #a[count, 0, 0] = float(x)
            #a[count, 0, 1] = float(y)
            tmp = np.array([x.round().astype(int),y.round().astype(int)])
            tmp = np.reshape(tmp, (1,2))
            
            a.append(tmp)     
            #count = count + 1
    if a != []:
        a = np.array(a)
        cv2.drawContours(mask, [a], -1, (0,255,0), thickness = -1)        
    else:
        for item in contour_list:
            item = np.array(item)
            cv2.drawContours(mask, [item], -1, (0,255,0), thickness = -1)
        
    #fig.savefig('/nfs/masi/leeh43/test.png')
    #cv2.fillPoly(mask, contours, 255)
    save_dir = os.path.join('/nfs/masi/leeh43/zhoubing100/img/' + img_num +'/')
    if os.path.isdir(save_dir) == False:
        os.mkdir(save_dir)
        
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    mask = cv2.resize(mask, None, None, fx=(1/scale), fy=(1/scale), interpolation=cv2.INTER_LINEAR)
    mask = cv2.resize(mask, (data_1.shape[1],data_1.shape[0]), fx=(1/im_scale), fy=(1/im_scale), interpolation=cv2.INTER_LINEAR)
    new_mask = np.zeros((512,512))
    new_mask[int(c[0]):int(c[1]) + 1, int(c[2]):int(c[3]) + 1] = mask
    aff_2 = aff_1[[1, 0, 2], :]
    if np.max(aff_2[1, :2]) > 0:
        new_mask[:, ::-1] = new_mask
    if np.max(aff_2[0, :2]) > 0:
        new_mask[::-1, :] = new_mask
    if np.abs(aff_1[0, 0]) > np.abs(aff_1[0, 1]):
        new_mask = np.transpose(new_mask)
    
    final_mask[:,:,i] = new_mask

    
output_fn_mask = os.path.join(save_dir + 'contour_mask.nii.gz')
#output_fn_img = os.path.join(save_dir + '100_slice_img.nii.gz')
mask_nifti = nib.Nifti1Image(final_mask, n.affine, n.header)
#img_nifti = nib.Nifti1Image(data_ori_100, n.affine, n.header)
nib.save(mask_nifti, output_fn_mask)
#nib.save(img_nifti, output_fn_img)