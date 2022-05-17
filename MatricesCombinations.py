import numpy as np
from Burrows0Wheeler import bwm_search
from SeedExtend import reverse_complement

def scoringMatrixCombination(x,y, match, mismatch, gap):  #making scoring matrix for each combination of values
     if (x=='_' or y=='_'): return gap
     if x==y: return match
     return mismatch

def globalAlignment_ex(x,y,s,match,mismatch, gap):  #like globalAlignment method defined in GlobalAlignment.py, but with other scoring
     D=np.zeros((len(x)+1,len(y)+1),dtype=int)     #values
     for i in range(1,len(x)+1):
        D[i,0]=D[i-1,0]+s(x[i-1],'_',match,mismatch, gap)
     for j in range(1,len(y)+1):
        D[0,j]=D[0,j-1]+s('_',y[j-1],match,mismatch, gap)
     for i in range(1,len(x)+1):
          for j in range(1, len(y)+1):
            D[i,j]=max(D[i-1,j]+s(x[i-1],'_',match,mismatch, gap), D[i,j-1]+s('_',y[j-1],match,mismatch, gap), D[i-1,j-1]+s(x[i-1],y[j-1],match,mismatch, gap))
     return D, D[len(x),len(y)]

def traceback_ex(x, y, D, s,match,mismatch, gap):   #like traceback method defined in GlobalAlignment.py, but with other scoring values
     tx=''
     ty=''
     t=''
     align=''
     i=len(x)
     j=len(y)
     
     while i>0 or j>0:
          d, h, v=-10000,-10000, -10000
          if i>0 and j>0:
               delta=0 if x[i-1]==y[j-1] else 1  
               d=D[i-1,j-1]+s(x[i-1],y[j-1],match,mismatch, gap)
          if i>0:
               v=D[i-1,j]+s(x[i-1],'_',match,mismatch, gap)
          if j>0:
               h=D[i,j-1]+s('_',y[j-1],match,mismatch, gap)
          if d>=h and d>=v:
               tx+=x[i-1]
               ty+=y[j-1]
               if delta==0:  
                    align+='|'
                    t+='M'
               else:
                    align+=' '
                    t+='R'
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


def seed_extend_comb(t, read, seed_length, margin, c, occ, suffix_arr, scoringMatrix, match,mismatch, gap):
     listAlign=[]   #same as seed_extend method in SeedExtend.py, but with scoring values to call methods for global alignment for these
     seed = read[0:seed_length]    #scoring values
     rc_read=reverse_complement(read)
     rc_seed=rc_read[0:seed_length]
     #print(read)
     #print(seed)
     index = bwm_search(seed, c, occ, suffix_arr)
     #print(index) #positions list
     #print(len(index))
     for pos in index:
          start=pos+seed_length
          end=start+(len(read)-seed_length)+margin
          end=len(t) if end>len(t) else end
          ref=t[start:end]
          read_truncated=read[seed_length:]
          #print(f'Seed:{seed}')
          #print(f'Read truncated:{read_truncated}')
          #print(f'Reference truncated:{ref}')
          D, alignmentScore=globalAlignment_ex(ref,read_truncated, scoringMatrix, match,mismatch, gap)
          #print(D)
          #print(alignmentScore)
          alignment, transcript=traceback_ex(ref, read_truncated, D, scoringMatrix, match,mismatch, gap)

          #print(alignment)
          #print(transcript)
          listAlign.append((read, pos, alignmentScore, transcript))
     index = bwm_search(rc_seed, c, occ, suffix_arr)
     for pos in index:
          start=pos+seed_length
          end=start+(len(rc_read)-seed_length)+margin
          end=len(t) if end>len(t) else end
          ref=t[start:end]
          read_truncated=rc_read[seed_length:]
          #print(f'Seed:{seed}')
          #print(f'Read truncated:{read_truncated}')
          #print(f'Reference truncated:{ref}')
          D, alignmentScore=globalAlignment_ex(ref,read_truncated, scoringMatrix, match,mismatch, gap)
          #print(D)
          #print(alignmentScore)
          alignment, transcript=traceback_ex(ref, read_truncated, D, scoringMatrix, match,mismatch, gap)

          #print(alignment)
          #print(transcript)
          listAlign.append((read, pos, alignmentScore, transcript))
     listAlign.sort(key=lambda el: el[2], reverse=True)
     return listAlign   
