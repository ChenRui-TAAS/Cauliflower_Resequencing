perl bin/slipping.pl Chr${i} length_of_Chr${i}        Group1 Group2 0 100000

python3 abstract_SlipingFst.py -i ../Group2_Group1/Chr${i}.fst.overall -chr Chr${i} -o ./Chr${i}.fst.overall_final

###then select top5 fst

###construct sweep regions
count_top_percent_5_divergence_region.py -i top_5_chr_pos_sort.fst -o sweep_regions.txt
