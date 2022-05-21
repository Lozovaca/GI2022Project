# Genome informatics project

## Tasks: ##
1) Creating an algorithm for index searching of strings using **Burrows-Wheeler transformation** and **FM-index**.
   This algorithm is made in **Burrows0Wheeler.py** file. There is made:
   - BW matrix
   - rotations
   - BWT by BWM
   - suffix array
   - BWT by suffix array
   - C-matrix
   - Occ-matrix
   - a method for index searching of position where a pattern matches to the text
2) Creating an algorithm for **Global Alignment** using **scoring matrix**.
   This algorithm is made in **GlobalAlignment.py** file. There is made:
   - scoring matrix
   - global alignment
   - traceback
3) Creating **Seed and Extend** method for a reference and reads.
   This algorithm is made in **SeedExtend.py** file. There is made:
   - a method for reading sequence of given reference
   - a method for reading given collection of reads
   - a method for Seed and Extend which returns tuples(start position, alignment score, edit transcript) by executing **index searching in BWT** for **seed part** and **Global Alignment** algorithm for **extend part**.
4) Comparing data, obtained from previous algorithms (a part below), with data obtained from **BWA-MEM tool** (b part below). 
      - a) There is a modification of scoring matches[0,1,2], missmatches[-3,-2] and gaps[-7,-5] in sequences, so this is made in **MatricesCombinations.py** file which is similar to previous files for **Global Alignment** and **Seed and extend**, but using each combination of scores. Testing this function and making plots and dataframes for all combinations is in notebook **Tests.ipynb** in the 4th part (from the 2nd cell bellow this heading).
      - Note: This part is okay with other reference and reads (example_human), but not with reference and reads for this project, we are not sure why this lasts so long in the stronger aws machine, even though a **Memory Error** occurs in the weaker aws machines...
      - b) SAM files for each combination of scores are made by command for executing **bwa mem tool** for given reference and reads, this is in file **sam_file_generete.py** which executes this tool called in a Docker image. Making plots and dataframes for .sam files is in notebook **SAMimport.ipynb**.
      - Note: Executing **bwa mem tool** is working for other combinations except where match equals zero, because it says assertion h0>0 failed in a file of this tool.
