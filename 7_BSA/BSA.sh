python3 different.py Cauli-ZB_Chr${i}.vcf CK-PQ435_Chr${i}.vcf P-Cau9-ast_Chr${i}.vcf CK18_Chr${i}.vcf diff_Cau9-CK18_Chr${i}.txt

python3 confidence_interval.py 03_20individuals.txt diff_Cau9-CK18_Chr${i}.txt confidence_Cau9-CK18_Chr${i}.txt

python3 sliding_windows.py Cauliflower_genome.fasta.len diff_Cau17-CK18_Chr${i}.txt 1000000 10000 Cau17-CK18_slip_Chr${i}.txt

python3 02_sliding_window_confidence_interval.py Cauliflower_genome.fasta.len confidence_Cau17-CK18_Chr${i}.txt 1000000 10000 confidence_Cau17-CK18_slip_Chr${i}.txt

