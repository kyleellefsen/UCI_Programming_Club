# -*- coding: utf-8 -*-
"""
Created on Fri May 08 20:11:28 2015

@author: Carley
"""

from __future__ import division
import matplotlib.pyplot as plt 
import os
import numpy as np
from skimage.measure import label
from skimage.measure import regionprops

def calculate_background(short_list):
	'''uses the first 100 frames to calculate the median (background)'''
    bkgd=[]
    for files in short_list:
        image=plt.imread(os.path.join(direc,videos,files))
        image=np.mean(image,2)
        bkgd.append(image)
    return np.median(bkgd,axis=0)

def get_coordinates(single_jpeg):
	''' '''
    coordinate_list=[]
    image=plt.imread(os.path.join(direc,videos,single_jpeg))
    image=np.mean(image,2)
    frame=image-background
    thresh=frame<-50
    labelled=label(thresh)
    numObjects=np.max(labelled)
    props=regionprops(labelled)
    indices=[]
    for x in range(numObjects):
        indices.append((x,props[x]['area']))
    largest_object=sorted(indices,key=lambda index:index[1],reverse=True)[0]
    #this line will sort by area so that the largest object is first in the list
    #then you can find the index of that object and pull its centroid coordinates
    i=largest_object[0]
    coordinate_list.append(list(props[i]['centroid']))  
    return coordinate_list

def chamber_counts(coordinates):
  	''' '''
    xs=[]
    for items in coordinates:
        xs.append(items[1])
    positions=[]
    width=np.max(xs)
    divs=width/3
    rightBound=width-divs
    leftBound=width-(2*divs)
    left=0
    center=0
    right=0
    for items in xs:
        if items>rightBound:
            right+=1
        if items<leftBound:
            left+=1
        else:
            center+=1
    positions.append(left)
    positions.append(center)
    positions.append(right)
    return positions    

direc=r'D:\150508 OD pilot\testing'
folders=os.listdir(direc)
results_all=[]
for videos in folders:
    print videos
    files = os.listdir(direc+'\\'+videos)
    background = calculate_background(files[:100])
    results = []
    for jpgs in files:
        coords = get_coordinates(jpgs)
        results.append(coords)
    results_all.append(results)
