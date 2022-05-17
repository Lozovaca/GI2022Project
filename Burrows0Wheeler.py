def rotations(t):
 ## Return list of rotations of input string t """
 tt = t * 2
 return [tt[i:i+len(t)] for i in range(0, len(t)) ]

def bwm(t):
### Return lexicographically sorted list of t’s rotations """
    return sorted(rotations(t))

def bwtViaBwm(t):
### Given T, returns BWT(T) by creating BWM """
    return ''.join(map(lambda x: x[-1], bwm(t)))

def firstColumnBwm(t):
### Given T, returns BWT(T) by creating BWM """
    return ''.join(map(lambda x: x[0], bwm(t)))

def suffixArray(s):
    """ Given T return suffix array SA(T). We use Python's sorted
    function here for simplicity, but we can do better. """
    satups = sorted([(s[i:], i) for i in range(len(s))])
    # Extract and return just the offsets
    return list(map(lambda x: x[1], satups))
def bwtViaSa(t):
    """ Given T, returns BWT(T) by way of the suffix array. """
    bw = []
    for si in suffixArray(t):
        if si == 0: bw.append('$')
        else: bw.append(t[si-1])
    return ''.join(bw) # return string-ized version of list bw

def rankBwt(bw):
    ''' Given BWT string bw, return parallel list of B-ranks.  Also
        returns tots: map from character to # times it appears. '''
    tots = dict()
    ranks = []
    for c in bw:
        if c not in tots: tots[c] = 0
        ranks.append(tots[c])
        tots[c] += 1
    return ranks, tots
def firstCol(tots):
    ''' Return map from character to the range of rows prefixed by
        the character. '''
    first = {}
    totc = 0
    for c, count in sorted(tots.items()):
        first[c] = (totc, totc + count)
        totc += count
    return first

def reverseBwt(bw):
    ''' Make T from BWT(T) '''
    ranks, tots = rankBwt(bw)
    first = firstCol(tots)
    rowi = 0 # start in first row
    t = '$' # start with rightmost character
    while bw[rowi] != '$':
        c = bw[rowi]
        t = c + t # prepend to answer
        # jump to row that starts with c of same rank
        rowi = first[c][0] + ranks[rowi]
    return t
    
def c_matrix_insert(t):  #creating C matrix for positions of the first appearance 
    firstCols=sorted(firstColumnBwm(t))   #of each character in the string of first columns of BWT matrix 
    c_matrix={}
    for i in range(len(firstCols)-1):
        if i==0: c_matrix[firstCols[i]]=i  #if it's a character '$', put 0th position
        if firstCols[i-1]!=firstCols[i]:  c_matrix[firstCols[i]]=i  #if these are other characters
    return c_matrix 

def occ_matrix_insert(t): #creating Occ matrix where rows are characters from the first column of BWT matrix, columns are characters from 
                                                    #the last column of BWT matrix
    firstCols=firstColumnBwm(t) #making first column of BWT matrix
    bwt=bwtViaBwm(t)    #making last column of BWT matrix
    #occ=[[0 for _ in range(len(bwt))] for _ in range(len(firstCols))]
    occ={}
    firstCols=sorted(set(bwt))
    for nt in firstCols:
        occ[nt]=[0]*len(bwt)    #initializing with 0 in the rows of Occ matrix
    for j in range(len(firstCols)):
        val=0
        for i in range(len(bwt)):
            if firstCols[j]==bwt[i]: #if a character from the first column is a 
                val+=1               #character from the last column, add his appearance with 1
            occ[firstCols[j]][i]=val  #we put a number of appearances of each character in BWT
    return occ


#t = 'banana$'
#c=c_matrix_insert(t)
#occ=occ_matrix_insert(t)
#firstCols=firstColumnBwm(t)
#suffix_arr = list(suffixArray(t))     #testing


def bwm_search(query,c,occ,suffix_arr):  #a method of index search of positions where pattern query matches in text
                                        #which matrices and suffix array are made
    p=query[::-1]                       #we are going from the last character in pattern to the left, look at line 105, we are getting it
    start=0
    end=0
    keys_list=list(c)                   #geting characters of C matrix, actually keys
    for i in range(len(p)):
        character_c=p[i]               
        if i==0:                       #if it's the last character, we need the following positions where this character matches in
            start=c[character_c]+1     #BWT first column by C matrix 
            character_c_next=''        #start=C(c)+1   end=C(c+1)
            for j in range(len(c)):
                if j==len(c)-1: 
                    end=0
                    break
                elif keys_list[j]==character_c:  #finding the next character c in keys of C matrix 
                    character_c_next=keys_list[j+1]
                    end=c[character_c_next]
                    break
        else:
            start=c[character_c]+occ[character_c][start-1-1]+1   #if it isn't the last character, we need these positions: 
            end=c[character_c]+occ[character_c][end-1]        #start=C(c)+Occ(c,start-1)+1 end=C(c)+Occ(c,end)
    
    index_list = []
    for element in suffix_arr[start-1:end]:       #we are using suffix array to find the offset of matching of the pattern to the text
        index = element                          #these are positions where pattern matches to the parts of rotated characters of the text 
        index_list.append(index)

    return sorted(index_list)

#print(bwm_search('ana',c,occ,firstCols,suffix_arr))  #testing