#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 13:34:46 2019

@author: aik19
"""

from pathlib import Path
import nrrd
#from mayavi import mlab
from skimage import measure
from skimage import filters
import matplotlib.pyplot as plt
import numpy as np

firstfolder = 74124
folder = "/media/aik19/Seagate Backup Plus Drive/ICIE16_Analysis_V2/Stage1/rm_smallCC/"

image,header = nrrd.read(Path(folder+str(firstfolder)+".nrrd"))


imaget= image.T
labelledImage = measure.label(imaget, background=0)
labelledImage1 = measure.label(image,background=0)


objectmes = measure.regionprops(labelledImage1)
print(objectmes[3].centroid)
#print(objectmes[3].label)
#print(objectmes[1].coords)

#print(objectmes[3].centroid)



plt.imshow(labelledImage[0])
plt.figure()
plt.imshow(labelledImage1.T[0])
#plt.figure()
#plt.imshow(objectmes[0].image[0])


#all_labels = measure.label(image.T)






#blobs_labels = measure.label(image.T, background=0)
#blobs_labels = blobs_labels.astype('int8')
#t_blobs_labels = blobs_labels.T

#nrrd.write("74122.nrrd",t_blobs_labels )
#plt.figure(figsize=(9, 3.5))
#plt.subplot(131)
#plt.imshow(image.T[222], cmap='gray')
#plt.axis('off')
#plt.subplot(132)
#plt.imshow(all_labels[222], cmap='nipy_spectral')
#plt.axis('off')
#plt.subplot(133)
#plt.imshow(blobs_labels[222], cmap='nipy_spectral')
#plt.axis('off')

#plt.tight_layout()
#plt.show()
#image = io.imread("/media/aik19/Seagate Backup Plus Drive/ICIE16_Analysis_V2/Stage1/SegmentedStruts_tifs/74122/1")

#io.imshow(image)

#mlab.figure()
#mlab.contour3d(image, contours=[85])
#mlab.outline(color=(0, 0, 0))