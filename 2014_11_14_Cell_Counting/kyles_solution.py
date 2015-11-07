# -*- coding: utf-8 -*-
"""
Created on Mon Nov 03 09:11:48 2014

@author: Kyle Ellefsen
"""
#from pyqtgraph import show
from skimage.io import imread, imsave, imshow
from skimage.viewer import ImageViewer
from skimage.filter import gaussian_filter
import scipy
import csv
import os
import numpy as np


#######################################################
###      Load the image
#######################################################
directory='H:\histology_images'
filename='cells.tif'
full_filename=os.path.join(directory,filename)
image=imread(full_filename,plugin='tifffile')
image=image.astype(np.float64)  # We need to convert the image from int32 to float64 before we can apply the gaussian filter

#######################################################
###      Gaussian Blur and get local contrast
#######################################################
image_blur=gaussian_filter(image,sigma=7)
image_local=image-image_blur

#######################################################
###     Threshold
#######################################################
image_thresh=image_local>35


#######################################################
###      Remove all objects that are too small
#######################################################
def remove_small_blobs(image,smallest_blob_size=20):
    '''
    This function takes a binary image and excludes all the continuous 'True' regions below a certain size.    
    '''
    labeled_array, nFeatures=scipy.ndimage.measurements.label(image)
    B=np.copy(image.reshape(np.size(image))) 
    def exclude_small_blobs(val, pos):
        if len(pos)<=smallest_blob_size:
            B[pos]=0
    lbls = np.arange(1, nFeatures+1)
    scipy.ndimage.labeled_comprehension(image_thresh, labeled_array, lbls, exclude_small_blobs, float, 0, True)
    B=np.reshape(B,image_thresh.shape).astype('float64')
    return B
new_image_thresh=remove_small_blobs(image_thresh,60)


#######################################################
###      Count and get the position
#######################################################
labeled_array, nFeatures=scipy.ndimage.measurements.label(new_image_thresh)
mean_positions=[]
for i in np.arange(1,nFeatures+1):
    positions=np.argwhere(labeled_array==i)
    mean_pos=np.mean(positions,0)
    mean_positions.append(mean_pos)
mean_positions=np.array(mean_positions)

#######################################################
###      Save the results
#######################################################
newfile=os.path.join(directory,'nCells.csv')
with open(newfile,'wb') as csvfile:
    writer=csv.writer(csvfile)
    writer.writerows(mean_positions)