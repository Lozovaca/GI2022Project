import numpy as np
def scoringMatrix(x,y):
     if (x=='_' or y=='_'): return -7
     if x==y: return 1
     minb, maxb=min(x,y), max(x,y),
     if (minb=='C' and maxb=='T'): return -1
     if (minb=='A' and maxb=='G'): return -1
     return -3
def globalAlignment(x,y,s):
     D=np.zeros((len(x)+1,len(y)+1),dtype=int)
     for i in range(1,len(x)+1):
        D[i,0]=D[i-1,0]+s(x[i-1],'_')
     for j in range(1,len(y)+1):
        D[0,j]=D[0,j-1]+s('_',y[j-1])
     for i in range(1,len(x)+1):
          for j in range(1, len(y)+1):
            D[i,j]=max(D[i-1,j]+s(x[i-1],'_'), D[i,j-1]+s('_',y[j-1]), D[i-1,j-1]+s(x[i-1],y[j-1]))
     return D, D[len(x),len(y)]

def traceback(x, y, D, s):
     tx=''
     ty=''
     t=''
     align=''
     i=len(x)
     j=len(y)
     while i>0 or j>0:
          d, h, v=-100,-100, -100
          if i>0 and j>0:
               d=D[i-1,j-1]+s(x[i-1],y[j-1])
          if i>0:
               v=D[i-1,j]+s(x[i-1],'_')
          if j>0:
               h=D[i,j-1]+s('_',y[j-1])
          if d>=h and d>=v:
               delta=0 if x[i-1]==y[j-1] else 1  
               if delta==0:  
                    align+='|'
                    t+='M'
               else:
                    align+=' '
                    t+='R'
               tx+=x[i-1]
               ty+=y[j-1]
               i-=1
               j-=1
          elif h>=v:
               t+='I'
               tx+='_'
               ty+=y[j-1]
               align+=' '
               j-=1
          else:
               t+='D'
               tx+=x[i-1]
               ty+='_'
               i-=1
               align+=' '
     a='\n'.join([tx[::-1], align[::-1], ty[::-1]])
     return a, t[::-1]

#x='TACGTCAGC'
#y='TATGTCATGC'
x='AGGTTTAAAAGGAAATAACTTTAAGCATGTGTCTAAATAGCAAGTAATGTTTTAGAGCGGATTCTCTTAAATTCAGCTT'
y='AGGAACCATAGCCATTGAAATGGATGAGGGAACCTATATACATGCACTCGACAATGGCCTTTTTACCCTGGGAGCT'
D, alignmentScore=globalAlignment(x,y,scoringMatrix)
alignment, transcript=traceback(x,y, D, scoringMatrix)
print(D)
print(alignmentScore)
print(alignment)
print(transcript)
