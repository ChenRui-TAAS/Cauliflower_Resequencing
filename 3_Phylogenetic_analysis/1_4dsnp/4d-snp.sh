perl loci_4d.pl genome.gff genome.fasta > cds.4d

perl same.pl cds.4d snps.geno ${Chr} > ${Chr}.4d.snp

filter_more_missing_and_maf_site.py -i ${Chr}.4d.snp -o ${Chr}4d.Maf0.05Miss0.2.snp
