import argparse
from Burrows0Wheeler import c_matrix_insert,occ_matrix_insert,firstColumnBwm,bwm_search,suffixArray
from Bio import SeqIO
from GlobalAlignment import globalAlignment, traceback, scoringMatrix

def readFASTA(fasta_file):
    arr = []
    for seq_record in SeqIO.parse(fasta_file, "fasta"):
        arr.append(seq_record.seq)
    return arr[0]

def readFASTQ(fastq_file):
    arr = []
    for seq_record in SeqIO.parse(fastq_file, "fastq"):
        arr.append(seq_record.seq)
    return arr




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


fasta_file = "./example_human_reference.fasta"
fastq_file = "./example_human_illumina.pe_1.fastq"
seed_length = 3
margin=3

t = readFASTA(fasta_file)
t+='$'
c = c_matrix_insert(t)  
occ = occ_matrix_insert(t)
suffix_arr = list(suffixArray(t))    
firstCols = firstColumnBwm(t)  # HERE WE HAVE FM-INDEX OF OUR FASTA FILE
reads = readFASTQ(fastq_file)
listAlign=[]

for read in reads:
    seed = read[0:seed_length]
    print(seed)
    index = bwm_search(seed, c, occ, suffix_arr)
    print(index) #positions list
    #print(len(index))
    for pos in index:
        start=pos
        end=start+len(read)+margin
        ref=t[start:end]
        D, alignmentScore=globalAlignment(ref, read, scoringMatrix)
        alignment, transcript=traceback(ref, read, D, scoringMatrix)
        print(D)
        print(alignmentScore)
        print(alignment)
        print(transcript)
        listAlign.append((start, alignmentScore, transcript))
    #print(listAlign)
    





