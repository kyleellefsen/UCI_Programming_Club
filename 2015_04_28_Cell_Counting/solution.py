
import matplotlib.pyplot as plt #this is the package that reads in images and can display them
import numpy as np
from skimage import measure

img_array=plt.imread(image_file_path) #This reads images to arrays

#to toggle between RGB and gray images:
plt.gray() #grayscale
plt.jet() #color

#img_Array is a three color image

red=img_array[:,:,0]
green=img_array[:,:,1]
blue=img_array[:,:,2]

plt.imshow(img_array) #this displays images

#next we ned to threshold the cells out so first, look at the cells we want
#to threshold
plt.gray()
plt.imshow(blue)
#standard thresholding is to do some number of standard deviations above the mean
#but there are lots of ways to do this, this is just the shortest
mean_of_img=np.mean(blue)
stdev_of_img=np.std(blue)
thresholded_image=blue>(mean_of_img+stdev_of_img*2.5)#This line makes a bunch of True False, true is higher
#false is lower
plt.imshow(thresholded_image)

from skimage import measure

labelled=measure.label(thresholded_image)
#ifthat line is crashing on you
import skimage
labelled=skimage.morphology.label(thresholded_image)

#try plotting this
plt.imshow(labelled)
#should be a bunch of cells of varying intensity
cells=measure.regionprops(labelled)
#OR: Rob's version...
cells=np.max(labelled)


#cells is an object array which means we can't directly access it so we need to get the tratis we want
#check here for availablable traits http://scikit-image.org/docs/dev/api/skimage.measure.html#skimage.measure.regionprops
counts=len(cells)
for cell in cells:
    print cell['centroid']