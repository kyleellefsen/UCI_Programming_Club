# -*- coding: utf-8 -*-
"""
Created on Wed Dec 02 11:29:45 2015

@author: colorbox
"""
from __future__ import division
import matplotlib
import numpy as np
import random
import pylab
import copy as cp



rabbit_carry_capacity=500
initial_rabbits=100
rabbit_move=.03
rabbit_death_v_fox=1.0
rabbit_reproduction=0.1

initial_foxes=30
fox_move=.05
death_rate_of_fox_if_no_food=.1
fox_reproduction=.5

resolution_of_collision=0.02
res_squared=resolution_of_collision**2

class fox_c: #make a blank class we can store stuff in
    pass

class rabbit_c:
    pass

def update(rabbits,foxes):
    if len(rabbits)>0: #if there are rabbits
        for rabbit in rabbits: #update each rabbit
            rabbit.x+=pylab.uniform(-rabbit_move,rabbit_move) #add a random amount to the rabbit's x based off their 'move rate'
            if rabbit.x<0: #make sure theyare not past boundaries
                rabbit.x=0
            if rabbit.x>1:
                rabbit.x=1
            rabbit.y+=pylab.uniform(-rabbit_move,rabbit_move) #add a random amount to the rabbit's y based off their 'move rate'
            if rabbit.y<0:  #make sure theyare not past boundaries
                rabbit.y=0
            if rabbit.y>1:
                rabbit.y=1
            fox_neighbors=[fox for fox in foxes if ((fox.x-rabbit.x)**2+(fox.y-rabbit.y)**2)<res_squared] #see if any foxes are in resolutoin range
            if len(fox_neighbors)>0: #if there are nearby foxes
                if pylab.random()<rabbit_death_v_fox: #see if the rabbit dies
                    rabbits.remove(rabbit) #kill rabbit
                    continue #go back to top a dead rabbit cannot reproduce
            if pylab.random()<rabbit_reproduction and len(rabbits)<rabbit_carry_capacity: #otherwise see if rabbit can reproduce, let it go up to carrying capacity
                rabbits.append(cp.copy(rabbit)) #if reproduced, create a new rabbit in the same position as the old one                            
    if len(foxes)>0: #if there are foxes
        for fox in (foxes): #update each fox
            fox.y+=pylab.uniform(-fox_move,fox_move) #add a random amount to the fox's y based off their 'move rate'
            if fox.y<0: #make sure theyare not past boundaries
                fox.y=0
            if fox.y>1:
                fox.y=1
            fox.x+=pylab.uniform(-fox_move,fox_move)#add a random amount to the fox's x based off their 'move rate'
            if fox.x<0: #make sure theyare not past boundaries
                fox.x=0
            if fox.x>1:
                fox.x=1
            rabbit_neighbors=[rab for rab in rabbits if ((rab.x-fox.x)**2+(rab.y-fox.y)**2)<res_squared] #see if there is a rabbit in resolution range
            if len(rabbit_neighbors)==0: #if there are no rabbits
                if pylab.random()<death_rate_of_fox_if_no_food: #roll chance to see if fox dies
                    foxes.remove(fox) #kill fox
            else: #if there is a rabbit nearby
                if pylab.random()<fox_reproduction: #check tosee if fox has baby 
                    foxes.append(cp.copy(fox))#if yes make a new fox in the same postion as previous fox
    return rabbits,foxes #return the updated arrays
    
def draw(rabbits,foxes):
    x = [fox.x for fox in foxes] #get x of foxes
    y = [fox.y for fox in foxes] #ger y of foxes
    pylab.plot(x, y, 'ro') #draw foxes
    x = [rabbit.x for rabbit in rabbits] #get x of rabbits
    y = [rabbit.y for rabbit in rabbits] #get y of rabbits
    pylab.plot(x, y, 'b.') #draw rabbits
    pylab.xlim(0,1) #set limit as we don't let critters past 0 or 1
    pylab.ylim(0,1) #set limit as we don't let critters past 0 or 1

#here is our actual function    
foxes=[] #make empty fox list
for i in range(initial_foxes): #make the right number of foxes
    fox=fox_c() #each fox is a 'fox object'
    fox.x=random.random() #made at a random x 
    fox.y=random.random() #made at a random y
    foxes.append(fox) #add the new fox to the fox list
    
#repeat the fox process for rabbits
rabbits=[]
for i in range(initial_rabbits):
    rabbit=rabbit_c()
    rabbit.x=random.random()
    rabbit.y=random.random()
    rabbits.append(rabbit)

rabbit_count=[] #mpty list to monitor rabbit popultion
fox_count=[] #empty list to monitor fox population
steps=1000 #how many times we'll update
image_print=5 #how often we'll print image
for i in range(steps):
    rabbit_count.append(len(rabbits)) #count rabbits
    fox_count.append(len(foxes)) #count foxes
    rabbits,foxes=update(rabbits,foxes) #update everybody
    print i #let us know it's moving, this can be very important
    if i%image_print==0: #each time we hit a multiple of our image print number
        draw(rabbits,foxes) #draw the rabbits and foxes
        pylab.savefig(str(i)+'.jpg') #save the figure
        pylab.clf() #clear the figure
pylab.plot(rabbit_count, 'b-',fox_count,'r-')