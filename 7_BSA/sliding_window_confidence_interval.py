#!usr/bin/python3
#-- coding: utf-8 --

import os
import sys
import argparse
import re

parser = argparse.ArgumentParser(description = 'calculate the confidence interval with a sliding window for per chomosome')
parser.add_argument('i1', type = argparse.FileType('r'), help = 'the input file name')
parser.add_argument('i2', type = argparse.FileType('r'), help = 'the input file name')
parser.add_argument('win', type = int, help = 'the window size')
parser.add_argument('sliding', type = int, help = 'the sliding size')
parser.add_argument('o', type = argparse.FileType('w'), help = 'the output file name')
args=parser.parse_args()

args.o.write('#CHROM\tStart\tEnd\tnumber\t01P_L_95\t01P_H_95\t01P_L_99\t01P_H_99\t02P_L_95\t02P_H_95\t02P_L_99\t02P_H_99\t03P_L_95\t03P_H_95\t03P_L_99\t03P_H_99\tdelta_index\tP1_index\tP2_index\n')

first_list = []
second_list = []
dict_win = {}
for eachline in args.i1:
	if not eachline or '#' in eachline:
		continue
	first_list = eachline.strip().split()
	for j in range(0,int(first_list[1])//args.sliding + 1):
		start = j*args.sliding
		end = start + args.win
		dict_win[first_list[0]+'_'+str(start)+'_'+str(end)] = [0]
		dict_win[first_list[0]+'_'+str(start)+'_'+str(end)].append(0)
		dict_win[first_list[0]+'_'+str(start)+'_'+str(end)].append(0)
		dict_win[first_list[0]+'_'+str(start)+'_'+str(end)].append(0)
		dict_win[first_list[0]+'_'+str(start)+'_'+str(end)].append(0)
		dict_win[first_list[0]+'_'+str(start)+'_'+str(end)].append(0)
		dict_win[first_list[0]+'_'+str(start)+'_'+str(end)].append(0)
		dict_win[first_list[0]+'_'+str(start)+'_'+str(end)].append(0)
		dict_win[first_list[0]+'_'+str(start)+'_'+str(end)].append(0)
		dict_win[first_list[0]+'_'+str(start)+'_'+str(end)].append(0)
		dict_win[first_list[0]+'_'+str(start)+'_'+str(end)].append(0)
		dict_win[first_list[0]+'_'+str(start)+'_'+str(end)].append(0)
		dict_win[first_list[0]+'_'+str(start)+'_'+str(end)].append(0)
		dict_win[first_list[0]+'_'+str(start)+'_'+str(end)].append(0)
		dict_win[first_list[0]+'_'+str(start)+'_'+str(end)].append(0)
		dict_win[first_list[0]+'_'+str(start)+'_'+str(end)].append(0)
for eachline in args.i2:
	if not eachline or '#' in eachline:
		continue
	second_list = eachline.strip().split()
	value = int(second_list[1])//args.sliding + 1
	if value <= 100:
		for index in range(0,value):
			start = index*args.sliding
			end = start + args.win
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][0] += float(second_list[5])
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][1] += float(second_list[6])
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][2] += float(second_list[7])
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][3] += float(second_list[8])
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][4] += float(second_list[9])
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][5] += float(second_list[10])
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][6] += float(second_list[11])
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][7] += float(second_list[12])
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][8] += float(second_list[13])
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][9] += float(second_list[14])
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][10] += float(second_list[15])
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][11] += float(second_list[16])
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][12] += float(second_list[17])
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][13] += float(second_list[18])
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][14] += float(second_list[19])
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][15] += 1
	if value > 100:
		for index in range(value-100,value):
			start = index*args.sliding
			end = start + args.win
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][0] += float(second_list[5])
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][1] += float(second_list[6])
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][2] += float(second_list[7])
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][3] += float(second_list[8])
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][4] += float(second_list[9])
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][5] += float(second_list[10])
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][6] += float(second_list[11])
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][7] += float(second_list[12])
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][8] += float(second_list[13])
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][9] += float(second_list[14])
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][10] += float(second_list[15])
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][11] += float(second_list[16])
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][12] += float(second_list[17])
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][13] += float(second_list[18])
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][14] += float(second_list[19])
			dict_win[second_list[0]+'_'+str(start)+'_'+str(end)][15] += 1
for item in dict_win.keys():
	number = dict_win[item][15]
	if number == 0:
		continue
	else:
		o1P_L_95 = dict_win[item][0]/number
		o1P_H_95 = dict_win[item][1]/number
		o1P_L_99 = dict_win[item][2]/number
		o1P_H_99 = dict_win[item][3]/number
		o2P_L_95 = dict_win[item][4]/number
		o2P_H_95 = dict_win[item][5]/number
		o2P_L_99 = dict_win[item][6]/number
		o2P_H_99 = dict_win[item][7]/number
		o3P_L_95 = dict_win[item][8]/number
		o3P_H_95 = dict_win[item][9]/number
		o3P_L_99 = dict_win[item][10]/number
		o3P_H_99 = dict_win[item][11]/number
		delta_index = dict_win[item][12]/number
		P1_index = dict_win[item][13]/number
		P2_index = dict_win[item][14]/number
		id_list = re.split('_',item)
		args.o.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}\t{12}\t{13}\t{14}\t{15}\t{16}\t{17}\t{18}'.format(id_list[0],id_list[1],id_list[2],number,o1P_L_95,o1P_H_95,o1P_L_99,o1P_H_99,o2P_L_95,o2P_H_95,o2P_L_99,o2P_H_99,o3P_L_95,o3P_H_95,o3P_L_99,o3P_H_99,delta_index,P1_index,P2_index))
		args.o.write('\n')

args.i1.close()
args.i2.close()
args.o.close()


