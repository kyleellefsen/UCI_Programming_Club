# -*- coding: utf-8 -*-
"""
Created on Mon May  4 09:04:53 2015

"""

from __future__ import division
import matplotlib.pyplot as plt #this is the package that reads in images and can display them
import os
import numpy as np

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