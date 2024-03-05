#!usr/bin/python3
#CAUHorticulture    Yang Qinqin     2019/12/25
#-- coding: utf-8 --

import os
import sys
import re

i1 = open(sys.argv[1],'r')
i2 = open(sys.argv[2],'r')
output = open(sys.argv[3],'w')

output.write('#CHROM\tPOS\tDP(G35+448)\tDP(D+R)\tDP(total)\t01P_L_95\t01P_H_95\t01P_L_99\t01P_H_99\t02P_L_95\t02P_H_95\t02P_L_99\t02P_H_99\t03P_L_95\t03P_H_95\t03P_L_99\t03P_H_99\tdelta_index\tP1_index\tP2_index\n')

dict_confi = {}
first_list = []
for eachline in i1:
	if not eachline:
		continue
	first_list = eachline.strip().split()
	dict_confi[first_list[0]] = [first_list[1]]
	dict_confi[first_list[0]].append(first_list[2])
	dict_confi[first_list[0]].append(first_list[3])
	dict_confi[first_list[0]].append(first_list[4])

second_list = []
third_list = []
for eachline in i2:
	if not eachline or '#' in eachline or 'CHROM' in eachline:
		continue
	second_list = eachline.strip().split()
	third_list = re.split('/',second_list[5])
	third_list[0] = re.split('\.',third_list[0])[0]
	third_list[1] = re.split('\.',third_list[1])[0]
	third_list[2] = re.split('\.',third_list[2])[0]
	third_list[3] = re.split('\.',third_list[3])[0]
	DP1 = (int(third_list[0])+int(third_list[1]))//2
	DP2 = (int(third_list[2])+int(third_list[3]))//2
	DP3 = (int(third_list[0])+int(third_list[1])+int(third_list[2])+int(third_list[3]))//4
	output.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}\t{12}\t{13}\t{14}\t{15}\t{16}\t{17}\t{18}\t{19}'.format(second_list[0],second_list[1],DP1,DP2,DP3,dict_confi[str(DP1)][0],dict_confi[str(DP1)][1],dict_confi[str(DP1)][2],dict_confi[str(DP1)][3],dict_confi[str(DP2)][0],dict_confi[str(DP2)][1],dict_confi[str(DP2)][2],dict_confi[str(DP2)][3],dict_confi[str(DP3)][0],dict_confi[str(DP3)][1],dict_confi[str(DP3)][2],dict_confi[str(DP3)][3],second_list[10],second_list[8],second_list[9]))
	output.write('\n')

i1.close()
i2.close()
output.close()

