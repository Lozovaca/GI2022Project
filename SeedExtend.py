import argparse

from Burrows0Wheeler import bwtViaBwm, c_matrix_insert,occ_matrix_insert,firstColumnBwm,bwm_search,suffixArray, rotations
from Bio import SeqIO
from GlobalAlignment import globalAlignment, traceback, scoringMatrix

def readFASTA(fasta_file):
    """arr = []
    for seq_record in SeqIO.parse(fasta_file, "fasta"):
        arr.append(seq_record.seq)
    return arr[0]"""
    return list(map(lambda f: str(f.seq), SeqIO.parse(fasta_file, "fasta")))

def readFASTQ(fastq_file):
    """arr = []
    for seq_record in SeqIO.parse(fastq_file, "fastq"):
        arr.append(seq_record.seq)
    return arr"""
    return list(map(lambda f: str(f.seq), SeqIO.parse(fastq_file, "fastq")))

def reverse_complement(read):
    rev_read=''
    for i in range(len(read)):
        if read[i]=='A': rev_read+='T'
        elif read[i]=='T': rev_read+='A'
        elif read[i]=='C': rev_read+='G'
        elif read[i]=='G': rev_read+='C'
    return rev_read[::-1]

#print(reverse_complement('AGAT'))

# parser = argparse.ArgumentParser()
# parser.add_argument("-R","--reference", help="reference to FASTA file",
#                     type=str)
# parser.add_argument("-C","--collection", help="read to FASTQ file",
#                     type=str)
# parser.add_argument("-S","--seed", help="length of seed",
#                     type=int)
# parser.add_argument("-M","--margin", help="margin",
#                     type=int)

# args = parser.parse_args()


#def seed_extend(t, reads, seed_length, margin):
fasta_file = "./example_human_reference.fasta"
fastq_file = "./example_human_Illumina.pe_1.fastq"
t = readFASTA(fasta_file)[0]
reads = readFASTQ(fastq_file)
seed_length = 3
margin = 3
t+='$' #necessary for test for bwt algorithm
c = c_matrix_insert(t)
occ = occ_matrix_insert(t)
suffix_arr = suffixArray(t)   
#firstCols = firstColumnBwm(t)  # HERE WE HAVE FM-INDEX OF OUR FASTA FILE
listAlign=[]
i=0
for read in reads:
    i+=1
    seed = read[0:seed_length]
    print(seed)
    index = bwm_search(seed, c, occ, suffix_arr)
    print(index) #positions list
    #print(len(index))
    for pos in index:
        start=pos+seed_length
        end=start+(len(read)-seed_length)+margin
        end=len(t) if end>len(t) else end
        ref=t[start:end]
        read_truncated=read[seed_length:]
        print(f'Seed:{seed}')
        print(f'Read truncated:{read_truncated}')
        print(f'Reference truncated:{ref}')
        D, alignmentScore=globalAlignment(ref,read_truncated, scoringMatrix)
        #print(D)
        #print(alignmentScore)
        alignment, transcript=traceback(ref, read_truncated, D, scoringMatrix)
       
        #print(alignment)
        #print(transcript)
        listAlign.append((pos, alignmentScore, transcript))
    if i==1: break
    

#listAlign=seed_extend(t, reads, seed_length, margin)
print(listAlign)



#fasta_file = "./reference.fasta"
#t = readFASTA(fasta_file)
#t+='$'
#print(rotations(t))"""