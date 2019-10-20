#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 10:27:09 2019

@author: leeh43
"""

import os 
import numpy as np

data_dir = os.path.join('/nfs/masi/leeh43/MULAN_universal_lesion_analysis/results/')
c_l = os.path.join(data_dir + '_nfs_masi_leeh43_zhoubing100_img_img0001.nii.gz/'
                   + 'contour_location.txt')
with open(c_l) as f:
    content = f.readlines()