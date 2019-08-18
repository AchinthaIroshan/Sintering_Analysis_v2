#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 13:45:35 2019

@author: aik19
"""


from pathlib import Path
import nrrd
from skimage import measure
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


firstfolder = 74122
folder = "/media/aik19/Seagate Backup Plus Drive/ICIE16_Analysis_V2/Stage1/rm_smallCC/"
outfolder1 = "/media/aik19/Seagate Backup Plus Drive/ICIE16_Analysis_V2/Stage1/centers_macro/"
outfolder2 = "/media/aik19/Seagate Backup Plus Drive/ICIE16_Analysis_V2/Stage1/centers_micro/"
outfolder3 = "/media/aik19/Seagate Backup Plus Drive/ICIE16_Analysis_V2/Stage1/labeled struts/"


def centerFinder(firstfolder,folder,outfolder1,outfolder2,outfolder3):

    cfobjects1 = {}
    cfobjects2 = {} 
    centers_df1 = {}
    centers_df2 = {}
    
    for i in range(5):
        folder_num = firstfolder + i 
        image,header = nrrd.read(Path(folder+str(folder_num)+".nrrd"))

        labelledImage = measure.label(image,background=0)
        
        nrrd.write(outfolder3+str(folder_num)+".nrrd",np.float32(labelledImage) )
        objectmes = measure.regionprops(labelledImage)
        for j in range(len(objectmes)):
            objectlabel = objectmes[j].label
            obejectName = "object"+str(objectlabel)
            lst = objectmes[j].centroid
            lst1 =[round(x) for x in lst]
            lst2 =[round(x*4) for x in lst]
            cfobjects1.update({obejectName:lst1})
            cfobjects2.update({obejectName:lst2})
        df1 = pd.DataFrame(cfobjects1,index=['x','y','z'])
        df2 = pd.DataFrame(cfobjects2,index=['x','y','z'])
        centers_df1[folder_num]=df1
        centers_df2[folder_num]=df2
        df1.to_csv(outfolder1+str(folder_num)+".csv", index=False)
        df2.to_csv(outfolder2+str(folder_num)+".csv", index=False)
        
    for key in centers_df1.keys():
        print("\n" +"="*40)
        print(key)
        print("-"*40)
        print(centers_df1[key])


#centerFinder(firstfolder,folder,outfolder1,outfolder2,outfolder3)
def f(x, y):
    return np.sin(np.sqrt(x ** 2 + y ** 2))

def plot3D():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = np.array([1,1,5,5,1,1,5,5,1,1,5,5])
    y = np.array([1,5,5,1,1,5,5,1,1,5,5,1])
    z = np.array([1,1,1,1,3,3,3,3,5,5,5,5])
    X, Y = np.meshgrid(x, y)
    Y, Z = np.meshgrid(y, z)

    ax.plot_wireframe(X, Y, Z, color='black')
    ax.set_title('wireframe')
    
#plot3D()

def plotCenters():
    
    data = pd.read_csv("/media/aik19/Seagate Backup Plus Drive/ICIE16_Analysis_V2/Stage1/centers_micro/74122.csv") 
    
    Row_list =[]
    
    for index, rows in data.iterrows(): 
        my_list =[rows.object1,
                  #rows.object2,
                  rows.object3,
                  #rows.object4,
                  #rows.object5,
                  #rows.object6,
                  rows.object7, 
                  #rows.object8, 
                  rows.object9, 
                  #rows.object10, 
                  #rows.object11, 
                  #rows.object12,
                  #rows.object13, 
                  #rows.object14, 
                  #rows.object15, 
                  #rows.object16, 
                  #rows.object17, 
                  #rows.object18,
                  #rows.object19, 
                  #rows.object20, 
                  #rows.object21, 
                  rows.object22, 
                  #rows.object23, 
                  rows.object24,
                  rows.object25,
                  #rows.object26,
                  rows.object27
                  ] 
        Row_list.append(my_list) 
         
    x = np.array(Row_list[0])
    y = np.array(Row_list[1])
    z = np.array(Row_list[2])
    
    X,Y = np.meshgrid(x, y)
    Y, Z = np.meshgrid(y, z)
    
    box= []
    
    for index, rows in data.iterrows(): 
        my_list =[rows.object1,
                  rows.object3,
                  rows.object7,  
                  rows.object9,  
                  rows.object22, 
                  rows.object24,
                  rows.object25,
                  rows.object27,
                  rows.object1,
                  rows.object3,
                  ] 
        box.append(my_list) 
    
    
    x_1 = np.array(box[0])
    y_1 = np.array(box[1])
    z_1 = np.array(box[2])
    
    X_1,Y_1 = np.meshgrid(x_1, y_1)
    Y_1, Z_1 = np.meshgrid(y_1, z_1)
    
    
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #ax.scatter(X, Y, Z, color='black')
    
    ax.plot_wireframe(X_1, Y_1, Z_1, color='black')
    ax.set_xlabel('$X$')
    ax.set_ylabel('$Y$')
    ax.set_zlabel('$Z$')


plotCenters()

#plot3D()
        
    
    

