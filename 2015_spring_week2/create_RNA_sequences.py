# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 06:36:48 2015

@author: kyle
"""
import numpy as np
from random import randint, shuffle

bases=['A','C','T','G']
strands=[]
for i in np.arange(10): #I'm making 10 RNA strands
    strand=[]
    for j in np.arange(randint(80,120)):  #Each one will be a random length between 80 and 120 base pairs
        base=bases[randint(0,3)]
        strand.append(base)
    strands.append(strand)
        
""" Now we have 10 strands.  I will make 10 copies of each strand, but each copy will have 0, 1, or 2 errors"""

imperfect_strands=[]
for strand in strands:
    for i in np.arange(10):
        strand=strand[:] #this copies the list.  It prevents us from overwriting the original
        for errorN in np.arange(randint(1,3)): # this loops through 1, or 2 times
            error_spot=randint(0,len(strand)-1)
            strand[error_spot]=bases[randint(0,3)]
        imperfect_strands.append(strand)

''' Mix up the strands '''
shuffle(imperfect_strands)
        
''' Now we convert our list of lists to a list of strings '''
output=''
for strand in imperfect_strands:
    output=output+''.join(strand)
    output=output+'\n'

''' Save the output '''

f = open("RNA_sequence.txt", "w")
f.write(output)
f.close()