# -*- coding: utf-8 -*-
from __future__ import division
import matplotlib.pyplot as plt #this is the package that reads in images and can display them
import matplotlib
import numpy as np
from pyqtgraph import show
import pyqtgraph as pg
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from scipy import spatial
import os

def getHigherPoint(ii,mask,center):
    position=np.unravel_index(ii,(mx,my))
    x,y=position
    density=C[position]          
    center2=np.copy(center)
    x0=x-center2[0]
    xf=x+center2[0]+1
    y0=y-center2[1]
    yf=y+center2[1]+1
    mask2=np.copy(mask)
    if x0<0:
        mask2=mask2[center2[0]-x:,:]
        center2[0]=x
        x0=0
    elif xf>mx:
        crop=-(xf-mx)
        if crop<0:
           mask2=mask2[:crop,:]
        xf=mx
    if y0<0:
        mask2=mask2[:,center2[1]-y:]
        center2[1]=y
        y0=0
    elif yf>my:
        crop=-(yf-my)
        if crop<0:
           mask2=mask2[:,:crop]
        yf=my
    densities=mask2*C[x0:xf,y0:yf]
    positions=np.array(np.where(densities>C[x,y])).astype(float).T-center2
    if len(positions)==0:
        return None
    distances=np.sqrt(positions[:,0]**2+positions[:,1]**2)
    min_dist=np.min(distances)
    min_dist_pixls=np.argwhere(min_dist==distances)
    if len(min_dist_pixls)==1:
        higher_pt=positions[min_dist_pixls[0]].astype(np.int)+np.array([x0,y0])+center2
        higher_pt=np.squeeze(higher_pt)
    else: #we need to find the most dense pixel because there is a distance tie
       pix_idxs=(positions[np.squeeze(min_dist_pixls)]+center2).astype(np.int)
       pix_idxs2=(pix_idxs[:,0],pix_idxs[:,1])
       densest=np.argmax(densities[pix_idxs2])
       higher_pt=pix_idxs[densest,:]+np.array([x0,y0])
    higher_pt=np.ravel_multi_index((higher_pt[0],higher_pt[1]),(mx,my))
    return [np.min(distances), higher_pt, density]
    
def getDensities(Image,threshold,mask_radius):
    B=np.zeros(Image.shape)
    Image_binary=Image>threshold
    mask,center=getMask(mask_radius,mask_radius)
    pxls=np.array(np.where(Image_binary)).T
    percent=0
    for i,pxl in enumerate(pxls):
        if percent<int(100*i/len(pxls)):
            percent=int(100*i/len(pxls))
            print('Calculating Densities  {}%'.format(percent))
        x,y=pxl
        try:
            B[x,y]=np.count_nonzero(mask*Image_binary[x-center[0]:x+center[0]+1,y-center[1]:y+center[1]+1])#*Image[x,y]
        except ValueError:
            mask2=np.copy(mask)
            center2=np.copy(center)
            x0=x-center2[0]
            xf=x+center2[0]+1
            y0=y-center2[1]
            yf=y+center2[1]+1
            if x0<0:
                mask2=mask2[center2[0]-x:,:]
                x0=0
            if y0<0:
                mask2=mask2[:,center2[1]-y:]
                y0=0
            if xf>mx-1:
                mask2=mask2[:-(xf-mx+1),:]
                xf=mx-1
            if yf>my-1:
                mask2=mask2[:,:-(yf-my+1)]
                yf=my-1
            B[x,y]=np.count_nonzero(mask2*Image_binary[x0:xf,y0:yf])#*Image[x,y]
    return B
        
def getMask(nx=15,ny=15):
    ''' nx and ny must be odd'''
    mask=np.zeros((nx,ny))
    if nx%2==0 or ny%2==0:
        print('get mask only accepts odd numbers.  Change nx or ny to an odd number')
        return False
    center=np.array([ (nx-1)/2, (ny-1)/2]).astype(np.int)
    for j in np.arange(mask.shape[0]):
        for k in np.arange(mask.shape[1]):
            if ((j-center[0])**2)/center[0]**2 + ((k-center[1])**2)/center[1]**2 <= 1:
                mask[j,k]=1
    return mask, center
    
class Point():
    def __init__(self,idx):
        self.children=[]
        self.idx=idx
    def __repr__(self):
        return str(self.idx)
    def getDescendants(self):
        self.descendants=self.children[:]
        for child in self.children:
            self.descendants.extend(child.getDescendants())
        return self.descendants
    
os.chdir('C:\\Users\\Kyle Ellefsen\\Documents\\GitHub\\ParkerLab\\FLIKA\\PyFLIKA2')
from FLIKA import *
app = QApplication(sys.argv)
initializeMainGui()
open_file(r'C:\Users\Kyle Ellefsen\Documents\GitHub\UCI_Programming_Club\2015_spring_week4\blue.tif')
C=g.m.currentWindow.image
mx,my=C.shape
C=getDensities(C,10,35)
Window(C)
D=np.linspace(0,.5,mx*my)
C=C+D.reshape(C.shape)
idxs=np.arange(mx*my)

""""
STRUCTURE OF HIGHER_PTS:
['Distance to next highest point, index of higher point, value of current point']
"""
higher_pts=np.zeros((len(idxs),3))
remander=np.arange(len(idxs))
percentOn=True
percent=0
for r in np.arange(15,51,2):
    print('Finding all higher points in radius {}'.format(r))
    mask,center=getMask(r,r)
    oldremander=remander
    remander=[]
    for loop_i, ii in enumerate(oldremander):
        if percentOn and percent<int(100*ii/len(oldremander)):
            percent=int(100*ii/len(oldremander))
            print('Calculating Densities  {}%'.format(percent))
        position=np.unravel_index(ii,(mx,my))
        if C[position]>0:
            higher_pt=getHigherPoint(ii,mask,center)
            if higher_pt is not None:
                higher_pts[ii]=higher_pt
            else:
                remander.append(ii)
    percentOn=False

maxDistance=np.sqrt(2*r**2)
if len(remander)==1:
    ii=remander[0]
    position=np.unravel_index(ii,(mx,my))
    density=C[position]          
    higher_pts[ii]=[maxDistance, ii, density]
elif len(remander)>1:
    idxs2=np.unravel_index(remander,(mx,my))
    idxs2=np.array(idxs2).T
    densities=C[idxs2[:,0],idxs2[:,1]]
    D=spatial.distance_matrix(idxs2,idxs2)
    for pt in np.arange(len(D)):
        dd=D[pt,:]
        order_of_distance=np.argsort(dd)
        densities_sorted_by_distance=densities[order_of_distance]
        order_of_higher_density_point=order_of_distance[np.argmax(densities_sorted_by_distance>densities_sorted_by_distance[0])]
        higher_pt_idx=remander[order_of_higher_density_point]
        distance=D[pt,order_of_higher_density_point]
        density=C[tuple(idxs2[pt])]
        if distance==0:
            distance=maxDistance
        higher_pts[remander[pt]]=[distance, higher_pt_idx, density]


higher_pts_tmp=higher_pts[higher_pts[:,0]>1]
y=[d[0] for d in higher_pts_tmp] #smallest distance to higher point
x=[d[2] for d in higher_pts_tmp] # density 
pw=pg.PlotWidget()
pw.plot(x,y,pen=None, symbolBrush=QBrush(Qt.blue), symbol='o')
pw.plotItem.axes['left']['item'].setLabel('Smallest distance to denser point'); pw.plotItem.axes['bottom']['item'].setLabel('Density')
pw.show()

#
#big=np.argwhere(higher_pts[:,2]>40000)
#big=np.unravel_index(big,(mx,my))
#result=np.zeros((mx,my))
#result[big]=1
#Window(result)
##
#big=np.argwhere(higher_pts[:,0]>1)
#big=np.unravel_index(big,(mx,my))
#result=np.zeros((mx,my))
#result[big]=1
#Window(result)




centers=[]
outsideROI=[]
for i in np.arange(len(higher_pts)):
    y=higher_pts[i][0]#smallest distance to higher point
    x=higher_pts[i][2]# density 
    if (x>300 and y>10):
        centers.append(i)
    else:
        outsideROI.append(i)

        
higher_pts2=higher_pts[:,1].astype(np.int)
points=[Point(i) for i in np.arange(len(higher_pts2))]
loop=np.arange(len(higher_pts2))
loop=np.delete(loop,centers)
for i in loop:
    if higher_pts2[i]!=i:
        if higher_pts[i,2]>10:
            points[higher_pts2[i]].children.append(points[i])

clusters=[]
for center in centers:
    descendants=points[center].getDescendants()
    cluster=[d.idx for d in descendants]
    cluster=np.array(cluster+[center])
    clusters.append(cluster)

# This gets rid of clusters that contain very few True pixels
#centers_with_small_cluster=[]
#centers_with_large_cluster=[]
#cluster_sizes=np.array([len(c) for c in clusters])
#for i in np.arange(len(clusters),0,-1)-1:
#    if cluster_sizes[i]<10:  #this constant can be changed
#        centers_with_small_cluster.append(centers[i])
#        del clusters[i]
#    else:
#        centers_with_large_cluster.append(centers[i])

cluster_im=np.zeros((mx,my,4))
cmap=matplotlib.cm.gist_rainbow
for i in np.arange(len(clusters)):
    color=cmap(int(((i%15)*255./16)))#+np.random.randint(255./12)))
    for j in np.arange(len(clusters[i])):
        x,y=np.unravel_index(clusters[i][j],(mx,my))
        cluster_im[x,y,:]=color
Window(cluster_im)
    

