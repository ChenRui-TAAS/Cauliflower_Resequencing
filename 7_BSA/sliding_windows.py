#!usr/bin/python3
#CAUHorticulture    Yang Qinqin     2019/12/16
#-- coding: utf-8 --

import os
import sys
import argparse
import re

parser = argparse.ArgumentParser(description = 'calculate the index with a sliding window for per chomosome')
parser.add_argument('i1', type = argparse.FileType('r'), help = 'the input file name')
parser.add_argument('i2', type = argparse.FileType('r'), help = 'the input file name')
parser.add_argument('win', type = int, help = 'the window size')
parser.add_argument('sliding', type = int, help = 'the sliding size')
parser.add_argument('o', type = argparse.FileType('w'), help = 'the output file name')
args=parser.parse_args()

args.o.write('#CHROM\tStart\tEnd\tsnp_number\tQ51_index\tG35_index\tdelta_index\n')

first_list = []
second_list = []
dict_win = {}
for eachline in args.i1:
	first_list = eachline.strip().split()
	if not eachline or '#' in eachline:
		continue
	for j in range(0,int(first_list[1])//args.sliding + 1):
		start = j*args.sliding
		end = start + args.win 
		dict_win[first_list[0]+'_'+str(start)+'_'+str(end)] = [0]
		dict_win[first_list[0]+'_'+str(start)+'_'+str(end)].append(0)
		dict_win[first_list[0]+'_'+str(start)+'_'+str(end)].append(0)
for eachline in args.i2:
	second_list = eachline.strip().split()
	if not eachline or '#' in eachline or 'CHROM' in eachline:
		continue
	value = int(second_list[1])//args.sliding + 1
	if value <= 100:
		for index in range(0,value):
			start = index*args.sliding
			end = start + args.win
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][0] += float(second_list[8])
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][1] += float(second_list[9])
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][2] += 1
	if value > 100:
		for index in range(value-100,value):
			start = index*args.sliding
			end = start + args.win
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][0] += float(second_list[8])
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][1] += float(second_list[9])
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][2] += 1
for item in dict_win.keys():
	snp_number = dict_win[item][2]
	if snp_number == 0:
		continue
	else:
		Q51_index = dict_win[item][0]/snp_number
		G35_index = dict_win[item][1]/snp_number
		delta_index = G35_index-Q51_index
		id_list = re.split('_',item)
		args.o.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\n'.format(id_list[0],id_list[1],id_list[2],snp_number,Q51_index,G35_index,delta_index))
	
args.i1.close()
args.i2.close()
args.o.close()
