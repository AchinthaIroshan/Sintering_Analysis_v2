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


firstfolder = 74122
folder = "/media/aik19/Seagate Backup Plus Drive/ICIE16_Analysis_V2/Stage1/rm_smallCC/"
outfolder1 = "/media/aik19/Seagate Backup Plus Drive/ICIE16_Analysis_V2/Stage1/centers_macro/"
outfolder2 = "/media/aik19/Seagate Backup Plus Drive/ICIE16_Analysis_V2/Stage1/centers_micro/"


cfobjects1 = {}
cfobjects2 = {} 
centers_df1 = {}
centers_df2 = {}

for i in range(4):
    folder_num = firstfolder + i 
    image,header = nrrd.read(Path(folder+str(folder_num)+".nrrd"))
    labelledImage = measure.label(image,background=0)
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
    
    
    

