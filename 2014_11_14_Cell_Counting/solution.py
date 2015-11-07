import matplotlib.pyplot as plt
plt.gray()
import os


directory='/home/kyle/Desktop/'
filename='cells.tif'
full_filename=os.path.join(directory,filename)

#######################################################
###      Load the image
#######################################################
from skimage.io import imread, imsave, imshow
image=imread(full_filename,plugin='tifffile') #if you're on a mac, you may need an 'r' before the filename


#######################################################
###      Gaussian Blur
#######################################################

##DPLP'S CODE
import scipy as scipy
from scipy.ndimage.filters import gaussian_filter as snf
blurredarray = snf(image,2)
plt.imshow(blurredarray)

#thresholding
thresh=blurredarray>100
plt.imshow(thresh)

#counting
from skimage.measure import label
from skimage.measure import regionprops

thresh=image>100
labels=label(thresh)
props=regionprops(labels)
areas=[]
for i in range(len(props)):
    areas.append(props[i]['Area'])
sized=[]
#items=[x for x in props if x['Area']>75]
for items in areas:
    if items>75:
        sized.append(items)
print len(sized)

labeled_array, nFeatures=scipy.ndimage.measurements.label(thresh)

#before we print coordinates we need to get indices of cells of the proper area oh nooooooo
locations=[x['Centroid'] for x in items]

import csv

with open(out_file_name, 'wb') as csvfile:
	writer=csv.writer(csvfile)
    writer.writerows(locations)



