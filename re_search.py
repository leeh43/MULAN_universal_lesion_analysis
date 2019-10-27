#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 10:25:23 2019

@author: leeh43
"""

import os 
import numpy as np
import re

img_num = 'img0001'
data_dir = '/nfs/masi/leeh43/MULAN_universal_lesion_analysis/results'
img_dir = '_nfs_masi_leeh43_zhoubing100_img_' + img_num + '.nii.gz/'
result = os.path.join(data_dir, img_dir + 'results.txt' )

with open(result) as f:
    content = f.readlines()
content = [x.strip() for x in content]
for item in content:
    if item == '':
        content.remove(item)

pattern = re.compile(r'slice\wliver')

for item in content:
    matches = pattern.finditer(item)
    for match in matches:
        print(match)