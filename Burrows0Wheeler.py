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
    return map(lambda x: (x[0],x[1]), satups)
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
    
def c_matrix_insert(t):
    firstCols=firstColumnBwm(t)
    c_matrix={}
    for i in range(len(firstCols)-1):
        if i==0: c_matrix[firstCols[i]]=i
        if firstCols[i-1]!=firstCols[i]:  c_matrix[firstCols[i]]=i
    return c_matrix 

def occ_matrix_insert(t):
    firstCols=firstColumnBwm(t) #first column
    bwt=bwtViaBwm(t)    #last column
    #occ=[[0 for _ in range(len(bwt))] for _ in range(len(firstCols))]
    occ={}
    firstCols=sorted(set(bwt))
    for nt in firstCols:
        occ[nt]=[0]*len(bwt)
    for j in range(len(firstCols)):
        val=0
        for i in range(len(bwt)):
            if firstCols[j]==bwt[i]: 
                val+=1
            occ[firstCols[j]][i]=val
    return occ


# t = 'banana$'
# c=c_matrix_insert(t)  
# occ=occ_matrix_insert(t)
# firstCols=firstColumnBwm(t)
# suffix_arr = suffixArray(t)

def bwm_search(query,c,occ,firstCols,suffix_arr):
    p=query[::-1]
    start=0
    end=0
    for i in range(len(p)):
        character_c=p[i]
        if i==0:
            start=c[character_c]+1
            character_c_next=''
            for j in range(len(firstCols)):
                if firstCols[j-1]==character_c:
                    character_c_next=firstCols[j]
            end=c[character_c_next]
        else:
            start=c[character_c]+occ[character_c][start-1-1]+1
            end=c[character_c]+occ[character_c][end-1]
    
    index_list = []
    for element in list(suffix_arr)[start-1:end]:
        value, index = element
        index_list.append(index)

    return sorted(index_list)

