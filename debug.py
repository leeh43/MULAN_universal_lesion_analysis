#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 15:53:34 2019

@author: leeh43
"""

import os 
import nibabel.cmdline.ls
import nibabel as nib
#import cv2

nifti_deeplesion = os.path.join('/nfs/masi/leeh43/DeepLesion/Images_nifti/'
                                + '000001_03_01_058-118.nii.gz')
n = nib.load(nifti_deeplesion)
data = n.get_data()
r_1 = n.header.get_zooms()

nifti_zb = os.path.join('/nfs/masi/tangy5/share2_tangy5/tangy5/DeepAbo3D/experiment/data/zhoubing100/img/img0001.nii.gz')
n_zb = nib.load(nifti_zb)
data_zb = n_zb.get_data()
r_2 = n_zb.header.get_zooms()
#data_zb_resize = cv2.resize(data_zb, (512,512))


nifti_imagevu = os.path.join('/share2/leeh43/First_Round_Images/scan_2/image_2/'
                             + 'landab_109_1.2.124.113532.160.129.51.69.20070726.40748.12940586_6324.nii.gz')
n_imagevu = nib.load(nifti_imagevu)
data_imagevu = n_imagevu.get_data()
r_3 = n_imagevu.header.get_zooms()

nifti_LITS = os.path.join('/nfs/masi/leeh43/LITS_datasets/input_volumes_train/'
                          + 'volume-0.nii')
n_LITS = nib.load(nifti_LITS)
data_LITS = n_LITS.get_data()
r_4 = n_LITS.header.get_zooms()