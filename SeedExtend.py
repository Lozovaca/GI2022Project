import argparse

from Burrows0Wheeler import bwtViaBwm, c_matrix_insert,occ_matrix_insert,firstColumnBwm,bwm_search,suffixArray, rotations
from Bio import SeqIO
from GlobalAlignment import globalAlignment, traceback

def readFASTA(fasta_file):    #we are reading from the file .fasta to get a sequence for our reference
    """arr = []
    for seq_record in SeqIO.parse(fasta_file, "fasta"):
        arr.append(seq_record.seq)
    return arr[0]"""
    return list(map(lambda f: str(f.seq), SeqIO.parse(fasta_file, "fasta")))

def readFASTQ(fastq_file):    #we are reading from the file .fastq to get sequences for our list of reads
    """arr = []
    for seq_record in SeqIO.parse(fastq_file, "fastq"):
        arr.append(seq_record.seq)
    return arr"""
    return list(map(lambda f: str(f.seq), SeqIO.parse(fastq_file, "fastq")))

def reverse_complement(read):   #a method for making reversed complemented read for our known read
    rev_read=''
    for i in range(len(read)):           #complements of nucleotides
        if read[i]=='A': rev_read+='T'  #A->T
        elif read[i]=='T': rev_read+='A' #T->A
        elif read[i]=='C': rev_read+='G' #C->G
        elif read[i]=='G': rev_read+='C' #G->C
    return rev_read[::-1]   #reversing

#print(reverse_complement('AGAT'))  #testing

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


def seed_extend(t, read, seed_length, margin, c, occ, suffix_arr, scoringMatrix):  #a method seed_and_extend
    listAlign=[]
    seed = read[0:seed_length]   #we extract a seed from the part of the read which is long for seed_length nucleotides
    rc_read=reverse_complement(read)  #calling reverse_complement method to make reversed complemented read
    rc_seed=rc_read[0:seed_length]     #we extract a seed from the complemented read which has same number of nucleotides as seed_length 
    #print(seed)
    index = bwm_search(seed, c, occ, suffix_arr)  #calling bwm_search for seed as pattern in reference t
    #print(index) #positions list
    #print(len(index))
    for pos in index:             #going through the list of positions of matching seed to reference t
        start=pos+seed_length     #now we are going from the position start after position where seed matches to reference t
        end=start+(len(read)-seed_length)+margin  #to the position end which is made by adding the remainder of the read after seed part 
        end=len(t) if end>len(t) else end
        ref=t[start:end]   #we truncate reference from this position start ot this position end
        read_truncated=read[seed_length:]  #we truncate read from the seed part
        #print(f'Seed:{seed}')
        #print(f'Read truncated:{read_truncated}')
        #print(f'Reference truncated:{ref}')
        D, alignmentScore=globalAlignment(ref,read_truncated, scoringMatrix) #calling global alignment and traceback
        #print(D)
        #print(alignmentScore)
        alignment, transcript=traceback(ref, read_truncated, D, scoringMatrix) #getting D, alignment score, alignment and transcript
    
        #print(alignment)
        #print(transcript)
        listAlign.append((pos, alignmentScore, transcript)) #these are tuples (start positions of matching, alignment score, edit 
                                                            #transcript) for this read
    index = bwm_search(rc_seed, c, occ, suffix_arr)  #now we are doing with reversed complemented read, same steps as for normal read
    for pos in index:
        start=pos+seed_length
        end=start+(len(rc_read)-seed_length)+margin
        end=len(t) if end>len(t) else end
        ref=t[start:end]
        read_truncated=rc_read[seed_length:]
        #print(f'Seed:{seed}')
        #print(f'Read truncated:{read_truncated}')
        #print(f'Reference truncated:{ref}')
        D, alignmentScore=globalAlignment(ref,read_truncated, scoringMatrix)
        #print(D)
        #print(alignmentScore)
        alignment, transcript=traceback(ref, read_truncated, D, scoringMatrix)
    
        #print(alignment)
        #print(transcript)
        listAlign.append((pos, alignmentScore, transcript))
    listAlign.sort(key=lambda el: el[1], reverse=True) #sorting by the alignment score in the descending order
    return listAlign
