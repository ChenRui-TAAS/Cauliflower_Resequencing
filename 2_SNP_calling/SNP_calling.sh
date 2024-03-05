#Step1. Genome mapping
/path/to/bwa mem -t 8 -M -R "@RG\tID:$tag\tLB:$tag\tPL:Illumina\tPU:PE\tSM:$tag" /path/to/genome_index R1.fq.gz R2.fq.gz |samtools view -@ 8 -bS > $tag.bam

#Step2. BAM trimming
samtools quickcheck -v ./1_bam/*.bam > bad_bams.fofn && echo 'all ok' || echo 'some files failed check, see bad_bams.fofn'
samtools stats ./1_bam/$tag.bam > ./2_bam_stats/$tag.bam.stats
samtools sort -@ 8 ./1_bam/$tag.bam -o ./3_bam_sort/$tag.sort.bam
samtools view -@ 8 -q 30 -bS ./3_bam_sort/$tag.sort.bam > ./4_bam_q30/$tag.sort.q30.bam
gatk MarkDuplicates -I ./4_bam_q30/$tag.sort.q30.bam -O ./5_bam_MarkDup/$tag.sort.q30.markdup.bam -M ./5_bam_MarkDup/$tag.sort.q30.markdup.metrics -AS true
gatk ValidateSamFile -I ./5_bam_MarkDup/$tag.sort.q30.markdup.bam -O ./5_bam_MarkDup/$tag.sort.q30.markdup.bam.check
samtools index ./5_bam_MarkDup/$tag.sort.q30.markdup.bam

#Step3. GATK HaplotypeCaller
gatk HaplotypeCaller -R $genome_fa -ERC GVCF -I $tag.bam -O $tag.gvcf.gz 2> $tag.HaplotypeCaller.log

#Step4. Variant Calling
gatk CombineGVCFs -R $genome_fa --variant $sample01.gvcf.gz --variant $sample02.gvcf.gz --variant $sample03.gvcf.gz -O combined.gvcf.gz
gatk GenotypeGVCFs -R $genome_fa -V combined.gvcf.gz -O popu.vcf.gz
gatk SelectVariants -R $genome_fa -V popu.vcf.gz -O raw_indels.vcf.gz -select-type INDEL 2> SelectIndels.log
gatk VariantFiltration -R $genome_fa -V raw_indels.vcf.gz -O final_indels.vcf.gz --filter-expression "QD < 2.0 || FS > 200.0 || ReadPosRankSum < -20.0" --filter-name "InDelsfilter" 2> FilterIndels.log
zcat final_indels.vcf.gz | perl -ne 'print if /^#/ or /PASS/' | bgzip > final_indels_passed.vcf.gz
gatk SelectVariants -R $genome_fa -V popu.vcf.gz -O raw_snps.vcf.gz -select-type SNP 2> SelectSNPs.log
gatk VariantFiltration -R $genome_fa -V raw_snps.vcf.gz -O final_snps.vcf.gz --filter-expression "QD < 2.0 || MQ < 40.0 || FS > 60.0 || MQRankSum < -12.5 || ReadPosRankSum < -8.0" --filter-name "SNPsfilter" --cluster-size 3 --cluster-window-size 10 2> FilterSNPs.log
zcat final_snps.vcf.gz | perl -ne 'print if /^#/ or /PASS/' | bgzip > final_snps_passed.vcf.gz

