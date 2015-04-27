# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt #this is the package that reads in images and can display them
import numpy as np
from __future__ import division
plt.gray()
img_array=plt.imread('rat_Btub.jpg')
blue=img_array[:,:,2]
show(blue)
plt.imshow(blue)

C=blue
mx,my=C.shape
idxs=np.arange(mx,my)


def getHigherPoint(ii,mask,center):
    position=np.unravel_index(ii,(mx,my))
    x,y=position
    density=C[position]          
    center=np.copy(center)
    x0=x-center[0]
    xf=x+center[0]+1
    y0=y-center[1]
    yf=y+center[1]+1
    mask2=np.copy(mask)
    if x0<0:
        mask2=mask2[center[0]-x:,:]
        center[0]=x
        x0=0
    elif xf>mx-1:
        mask2=mask2[:-(xf-mx+1),:]
        xf=mx-1
    if y0<0:
        mask2=mask2[:,center[1]-y:]
        center[1]=y
        y0=0
    elif yf>my-1:
        mask2=mask2[:,:-(yf-my+1)]
        yf=my-1
    positions=np.array(np.where(mask2*C[x0:xf,y0:yf]>C[x,y])).astype(float).T-center
    if len(positions)==0:
        return None
    distances=np.sqrt(positions[:,0]**2+positions[:,1]**2)
    higher_pt=positions[np.argmin(distances)].astype(np.int)+np.array([x0,y0])+center
    higher_pt=C[zip(higher_pt)]
    return [np.min(distances), higher_pt, density]
        
def getMask(nx=15,ny=15):
    ''' nx and ny must be odd'''
    mask=np.zeros((nx,ny))
    center=np.array([ (nx-1)/2, (ny-1)/2]).astype(np.int)
    for j in np.arange(mask.shape[0]):
        for k in np.arange(mask.shape[1]):
            if ((j-center[0])**2)/center[0]**2 + ((k-center[1])**2)/center[1]**2 <= 1:
                mask[j,k]=1
    return mask, center


mask,center=getMask()
higher_pts=np.zeros((len(idxs),3))
for ii in np.arange(len(idxs)):
    higher_pt=getHigherPoint(ii,mask,center)
    if higher_pt is None:
        higher_pts.append(np.array([0,0,0]))
    else:
        higher_pts.append(higher_pt)
    