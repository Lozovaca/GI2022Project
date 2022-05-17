import numpy as np
def scoringMatrix(x,y):     #defining scoring matrix for match, transversion, transition, insertion and deletion
     if (x=='_' or y=='_'): return -7  #insertion and deletion
     if x==y: return 1    #matching
     minb, maxb=min(x,y), max(x,y),
     if (minb=='C' and maxb=='T'): return -1   #transition: C <-> T
     if (minb=='A' and maxb=='G'): return -1   #transition: A <-> G
     return -3  #transversion: other transformations of nucleotides
def globalAlignment(x,y,s):    #s is a scoring matrix, x is a reference, y is a read
     D=np.zeros((len(x)+1,len(y)+1),dtype=int)  #we are initializing D matrix with zeros
     for i in range(1,len(x)+1):
        D[i,0]=D[i-1,0]+s(x[i-1],'_')    #D(i,0)=D(i-1,0)+s(x[i-1],'_')
     for j in range(1,len(y)+1):
        D[0,j]=D[0,j-1]+s('_',y[j-1])    #D(0,j)=D(0,j-1)+s('_', y[j-1])
     for i in range(1,len(x)+1):
          for j in range(1, len(y)+1):
            D[i,j]=max(D[i-1,j]+s(x[i-1],'_'), D[i,j-1]+s('_',y[j-1]), D[i-1,j-1]+s(x[i-1],y[j-1]))
     return D, D[len(x),len(y)]  #making the final D-matrix and in the last row and in the last 
                                #column is an alignment score of matching the to the reference

def traceback(x, y, D, s):  #traceback method, s is a scoring matrix, x is a reference, y is a read, D is a D-matrix created in 
                            #globalAlignment method
     tx=''                #this is x reference with blanks if there's action Insertion
     ty=''                #this is y read with blanks if there's action Deletion 
     t=''                 #that's edit transcript of actions (Match, Mismatch-Replacing, Insertion, Deletion)
     align=''             #we are putting | if there' matching between characters of x and y
     i=len(x)
     j=len(y)
     
     while i>0 or j>0:
          d, h, v=-10000,-10000, -10000     #initialized values for diagonal, vertical and horizontal moving from the last row and
          if i>0 and j>0:                   #the last column to the first row and the first column
               delta=0 if x[i-1]==y[j-1] else 1  #if there's Match of characters of x and y, delta is 0
               d=D[i-1,j-1]+s(x[i-1],y[j-1])     #value of diagonal moving
          if i>0:
               v=D[i-1,j]+s(x[i-1],'_')           #value of vertical moving
          if j>0:
               h=D[i,j-1]+s('_',y[j-1])           #value of horizontal moving
          if d>=h and d>=v:                      #if d is greater than h and v, go diagonally left
               tx+=x[i-1]                        #getting character of x and y, to write them one below another in the alignment text
               ty+=y[j-1]                    
               if delta==0:                      # if it's Match, write |, and action is M
                    align+='|'
                    t+='M'
               else:
                    align+=' '                  #if it's not Match, write nothing, and action is Relacing
                    t+='R'
               i-=1
               j-=1
          elif h>=v:                          #if h is greater than v, go horizontally and action is Insertion
               t+='I'
               tx+='_'
               ty+=y[j-1]
               align+=' '
               j-=1
          else:                           #if v is greater than h, go vertically and action is Deletion
               t+='D'
               tx+=x[i-1]
               ty+='_'
               i-=1
               align+=' '
     a='\n'.join([tx[::-1], align[::-1], ty[::-1]])   #making alignment between x, and y characters
     return a, t[::-1]                               # return alignment and edit transcript of actions 


