import numpy as np
from pyqtgraph import show

RNA_filename=r'/Users/kyle/Github/UCI_Programming_Club/2015_spring_week2/RNA_sequence.txt'
RNA_file=open(RNA_filename)
RNA=[]
for line in RNA_file:
    RNA.append(line.strip('\n'))
RNA_file.close()
groups=[]

Diff=np.zeros((len(RNA),len(RNA)))
for i in np.arange(len(RNA)):
    for j in np.arange(len(RNA)):
        min_len=np.min([len(RNA[i]),len(RNA[j])])
        for cidx in np.arange(min_len):
            if RNA[i][cidx]==RNA[j][cidx]:
                Diff[i,j]+=1
#conor               
output=np.zeros([len(rnas),len(rnas)])
for idx, base in enumerate(rnas):
  for idx2,base2 in enumerate(rnas):
    if lengths[idx]==lengths[idx2]:
      test=0
      for iX in range(len(base)):
        test=test+base[iX]==base2[iX]
      output[idx,idx2]=test/len(base)
      
      
      
      