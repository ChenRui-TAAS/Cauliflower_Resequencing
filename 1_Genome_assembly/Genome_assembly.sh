#Step1. CANU Assembly
/path/to/canu -s pacbio.spec -p Cauli_C8 -d Cauli_C8 genomeSize=600m -pacbio-raw RawPacBio.fasta

Pacbio.spec:
useGrid = true;
minThreads = 4;
genomeSize = 600m;
minOverlapLength = 700;
minReadLength = 1000;

#Step2. BioNano Assembly
/path/to/pipelineCL.py -U -d -T 80 -j 8 -N 10 -i 3 -B 6 -a "Assembly.xml" "6700.6902rel" -l "./output/" -b "RawMolecules.bnx" -r "CANU.contigs_DLE_0kb_0labels.cmap" -y 2>&1 >> log.txt

#Step3. BioNano Scaffold
perl /path/to/scripts/HybridScaffold/hybridScaffold.pl
-n data/seq/input.fa
-b data/Bionano/exp_refineFinal1_contigs.cmap
-c data/hybridScaffold_config.xml
-r bin/RefAligner
-o data/hybridscaffold/output
-f
-B 2
-N 2
-x

#Step4. HERA
See details in https://github.com/liangclab/HERA

#Step5. Pilon Polishing
bwa index Cauli_C8_SuperContig.fasta
bwa mem -t 10 Cauli_C8_SuperContig.fasta R1.fastq.gz R2.fastq.gz | samtools sort -@ 10 -O bam -o align.bam
samtools index -@ 10 align.bam
samtools rmdup align.bam align_markdup.bam
samtools view -@ 10 -q 30 -b align_markdup.bam > align_filter.bam
samtools index align_filter.bam
java -jar -Xmx1000G pilon-1.22.jar --genome Cauli_C8_SuperContig.fasta --frags align_filter.bam --fix snps,indels --output pilon_polished --vcf --targets Name.txt &> pilon.log

#Step6. HiC
#Step6.1 JUICER
time sh ./scripts/juicer.sh \
        -D ./ \
        -d ./Assembly \
        -q lowb \
        -Q 250:00 \
        -l lowb \
        -L 250:00 \
        -C 100000000 \
        -s MboI \
        -g Cauli_C8 \
        -z ./references/Genome_Contigs.fasta \
        -p ./references/Cauli_C8.fasta.ref

#Step6.2 3DDNA
exepath=/public-supool/software/3d-dna/
export PATH=/public-supool/software/parallel-20180222/bin:$PATH
export PATH=/public-supool/software/jdk1.8.0_161/bin:$PATH

time ${exepath}/run-asm-pipeline.sh \
     Genome_Contigs.fasta \
     mnd.txt
