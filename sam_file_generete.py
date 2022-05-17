import os

match=[0,1,2]
mismatch=[-3, -2]
gap=[-7, -5]
seed_length = 10
reference_file = 'reference.fasta'
fastq_file = 'reads.fastq'
nthreads=1000

bash_command_index = '../bwa-0.7.15/bwa index '+ reference_file
os.system(bash_command_index)   #we are making cmd command for bwa mem tool to execute for each combination of scoring values, for giving number of threads and seed length (10)
for i in range(len(match)):     #first we are making index for reference
    m=match[i]
    for j in range(len(mismatch)):
        miss=mismatch[j]
        for k in range(len(gap)):
            g = gap[k]
            #bash_command ='../bwa-0.7.15/bwa mem -k ' + str(seed_length) +' -A '+ str(m) +' -B ' + str(miss) + ' -O ' + str(g) + ' '+ reference_file +' ' + fastq_file +' > sam_file{'+ str(m) + '}{' +  str(miss) + '}{' + str(g) + '}.sam';
            bash_command ='../bwa-0.7.15/bwa mem -t '+ str(nthreads) +' -A '+ str(m) +' -B ' + str(miss) + ' -O ' + str(g) + ' '+ reference_file +' ' + fastq_file +' > sam_file['+ str(m) + ',' +  str(miss) + ',' + str(g) + '].sam'
            #A is match score, B is mismatch score, O is gap score
            print(bash_command)   
            os.system(bash_command)

            # ./bwa mem -k seed_length  -A match   -B miss  -O gap  reference_file  fastq_file   > sam_file{m}{miss}{g}
