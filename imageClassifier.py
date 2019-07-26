#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 14:02:20 2019

@author: aik19
"""
from pathlib import Path
import nrrd
import numpy as np
from skimage.transform import resize
from joblib import load
import matplotlib.pyplot as plt

data,header = nrrd.read(Path("/home/aik19/Achintha/Sintering analysis/Macro Scale ICIE16/Preprocessed.nrrd"))
image = data.T
features = []
clf = load('classifier_svm.joblib') 
for slices in image:
     img_resized = resize(slices, (64,64), anti_aliasing=True, mode='reflect')   
     features.append(img_resized.flatten())
labels = clf.predict(features)
print(labels)   


z,y,x = image.shape

black = np.zeros((y,x))
#plt.imshow(black)
#plt.imshow(image[0])

for i in range(z):
    if labels[i] == 1:
        image[i] = black

nrrd.write('output1.nrrd', image.T)      
    
    




        
#get_image_features("/home/aik19/Achintha/Sintering analysis/Macro Scale ICIE16/Preprocessed")


    