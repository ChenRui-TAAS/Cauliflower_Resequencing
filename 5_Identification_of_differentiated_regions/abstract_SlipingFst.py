#!python3
#coding=utf-8
###program information###
#version: 1.0	author: chenke <answer514367672@163.com>	date: 2021-5-7

#include the required module
import sys
import os
import re
import argparse

#command-line interface setting
parser = argparse.ArgumentParser(description = 'Screening Fst from window')
parser.add_argument('-i', type = argparse.FileType('r'), help = 'FST output file overall')
parser.add_argument('-chr', type = str, help = 'Chromosome Number (Fst window file, such as Chr1)')
parser.add_argument('-o', type = argparse.FileType('w'), help = 'Output of Fst result file')

args = parser.parse_args()


sliping=""
fst=""
Chr=args.chr
for eachline1 in args.i:
	eachline1 = eachline1.strip()
	list1 = eachline1.split()
	if not eachline1 or eachline1[0] == "#":
		continue
	if '"' not in eachline1:
		sliping = eachline1
	#	print(eachline1)
	if '"' in eachline1:
		if list1[0] == '"Fst"':
			if list1[1] == "NA":
				args.o.write('{0}\t{1}\t0\n'.format(Chr,sliping))
			else:
				fst=abs(float(list1[1]))
				args.o.write('{0}\t{1}\t{2}\n'.format(Chr,sliping,fst))
		else:
			continue
