#!python3
#coding=utf-8
#This script is used to sliding windows

import re
import os
import sys
import argparse

parser = argparse.ArgumentParser(description = 'calculate the overlap rate with a sliding window for per chomosome')
parser.add_argument('-i1', type = argparse.FileType('r'), help = 'the input file name')
parser.add_argument('-i2', type = argparse.FileType('r'), help = 'the input file name')
parser.add_argument('-win', type = int, help = 'the window size')
parser.add_argument('-sliding', type = int, help = 'the sliding size')
parser.add_argument('-o', type = argparse.FileType('w'), help = 'the output file name')
parser.add_argument('-winNum', type = argparse.FileType('a'), help = 'all win number')
args=parser.parse_args()

args.o.write('#CHROM\tStart\tEnd\tidentity_number\tidentity_total\taveridentity_rate_inWINs\n')

list1 = []
list2 = []
dict_win = {}
overlap = int(args.win/args.sliding)
for eachline1 in args.i1:
	eachline1 = eachline1.strip()
	list1 = eachline1.split()
	args.winNum.write('{0}\n'.format(int(list1[1])//args.sliding + 1))
	if not eachline1 or eachline1[0] == "#":
		continue
	for i in range(0,int(list1[1])//args.sliding + 1):
		start = i*args.sliding
		end = start + args.win
		dict_win[list1[0]+'_'+str(start)+'_'+str(end)] = [0]
		dict_win[list1[0]+'_'+str(start)+'_'+str(end)].append(0)

for eachline2 in args.i2:
	eachline2 = eachline2.strip()
	list2 = eachline2.split('\t')
	if not eachline2 or eachline2[0] == "#":
		continue
	locus = int(list2[1])//args.sliding + 1
	if locus <= overlap:
		for j in range(0,locus):
			start = j*args.sliding
			end = start + args.win
			dict_win[list2[0]+'_'+str(start)+'_'+str(end)][0] += float(list2[2])
			dict_win[list2[0]+'_'+str(start)+'_'+str(end)][1] += 1
	if locus > overlap:
		for j in range(locus-overlap,locus):
			start = j*args.sliding
			end = start + args.win
			dict_win[list2[0]+'_'+str(start)+'_'+str(end)][0] += float(list2[2])
			dict_win[list2[0]+'_'+str(start)+'_'+str(end)][1] += 1

for item in dict_win.keys():
	identity_num = dict_win[item][1]
	if identity_num == 0:
		continue
	else:
		identity_rate = dict_win[item][0]/dict_win[item][1]
		if identity_rate >= 0.95:
			id_list=re.split('_',item)
			args.o.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(id_list[0],id_list[1],id_list[2],identity_num,dict_win[item][0],identity_rate))
