# -*- coding: utf-8 -*-
"""
Created on Mon May  4 09:04:53 2015

@author: kyle
"""

from __future__ import division
import matplotlib.pyplot as plt #this is the package that reads in images and can display them
import os
import numpy as np

os.chdir('/Users/kyle/Github/ParkerLab/FLIKA/PyFLIKA2/')
from FLIKA import *
app = QApplication(sys.argv)
initializeMainGui()


image_file_path='/Users/kyle/Github/UCI_Programming_Club/2015_spring_week5/mouse video/' #Replace this with your own path to the image directory
os.chdir(image_file_path) #now we are inside the directory which contains the images
file_names=os.listdir('.') #This creates a list containing all the files in the current directory.  The dot '.' represents the current directory
images=[]
for file_name in file_names:
  image=plt.imread(file_name)
  image=np.mean(image,2) # There are 3 dimensions, [x,y,color].  This averages over the third dimension.  
  images.append(image)
images=np.array(images)  
''' Now we have an array of images.  The array has dimensions [t,x,y].  We can pull out the first image and play with it. '''
image=images[0]
plt.gray()
plt.imshow(image)

''' Lets find the background by taking the median image '''
background=np.median(images,0) 
background_subtracted=images-background
thresholded=background_subtracted<-40

import numpy as np
import scipy
from scipy.ndimage.measurements import label
from process.file_ import open_file
from window import Window
    
def keepLargestBinary(image): # replace with skimage.morphology.remove_small_objects
    s=scipy.ndimage.generate_binary_structure(2,2)
    for i in np.arange(len(image)):
        labeled_array, num_features = label(image[i], structure=s)
        if num_features>1:
            lbls = np.arange(1, num_features+1)
            largest=0
            largest_lbl=0
            for lbl in lbls:
                length=np.count_nonzero(labeled_array==lbl)
                if length>largest:
                    largest=length
                    largest_lbl=lbl
            image[i]=labeled_array==largest_lbl
    return image

original=g.m.currentWindow
nFrames=len(original.image)
median=zproject(0,nFrames,'Median',keepSourceWindow=True)
original.image-=median.image
g.m.currentWindow=original
gaussian_blur(2)
threshold(-10,darkBackground=True)
image=keepLargestBinary(g.m.currentWindow.image)
Window(image)


#filename="D:/Old/Software/2014.05 motiontracking/t1_1.tif"
#original=open_file(g.m.settings['filename'])


"""
from PyQt4.QtCore import pyqtSlot as Slot
@Slot(int)
def updateTime(time):
    x0,y0,x1,y1=bbox[time]
    roi=g.m.currentWindow.currentROI
    roi.draw_from_points([(x0,y0),(x0,y1),(x1,y1),(x1,y0),(x0,y0)])
    roi.translate_done.emit()
    print(time)
bbox=np.zeros((len(image),4))
for i in np.arange(len(image)):
    B = np.argwhere(image[i])
    bbox[i,:]=np.concatenate((B.min(0),B.max(0)))
original.imageview.sigTimeChanged.connect(updateTime)
background=np.copy(g.m.currentWindow.image)
for i in np.arange(len(background)):
    x0,y0,x1,y1=bbox[i]
    for j in np.arange(i,len(background)): #j is the first index where the bounding boxes don't collide
        left,top,right,bottom=bbox[j]
        if (left>x1 or top>y1 or bottom<y0 or right<x0): #if the bounding boxes to not intersect
            break
    if j==len(background)-1:
        for j in np.arange(i,0,-1): #j is the first index where the bounding boxes don't collide
            left,top,right,bottom=bbox[j]
            if (left>x1 or top>y1 or bottom<y0 or right<x0): #if the bounding boxes to not intersect
                break
    background[i,x0:x1,y0:y1]=background[j,x0:x1,y0:y1]
show(background)
image=np.copy(g.m.currentWindow.image)
g.m.currentWindow.image=image-background; g.m.currentWindow.reset()
threshold(-27,darkBackground=True)
binary_dilation(2,1,1,keepSourceWindow=True)
g.m.currentWindow.image=keepLargestBinary(g.m.currentWindow.image)
g.m.currentWindow.reset()
"""
    
