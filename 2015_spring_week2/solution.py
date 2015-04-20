#http://www.sciencemag.org/content/347/6226/1138.full.pdf

#Carley's code to import the txt file into a python list

rnafile=r'/Users/ckarz030/Desktop/RNA_sequence.txt'
testfile=open(rnafile)
rna=[]
for lines in testfile:
    rna.append(lines)
    

#to figure out the number of unique sequence lengths:

lengths=[]
for items in rna:
	lengths.append(len(items))
uniques=sorted(set(lengths)) #the size of uniques = how many possible sequence lengths you have

#Conor's one-line method

lengths=[len(x) for x in rna]
#sort sequences by length, then compare them...?


''' KYLES SUPER COOL EASY FAST AWESOME WAY: '''
RNA_filename=r'/home/kyle/Desktop/RNA_sequence.txt'
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
      
      
      
      