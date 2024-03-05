#!/public/agis/huangsanwen_group/lintao/bin/python3
#program name: divergence_regions.py
##program information###
#version: 1.0	author: lintao <lintao19870305@gmail.com>	date: 2013-11-07

#include the required module
import sys
import os
import re
import argparse

#command-line interface setting
parser = argparse.ArgumentParser(description = 'Screening divergence regions')
parser.add_argument('-i', type = argparse.FileType('r'), help = 'Input of top 5 file')
parser.add_argument('-o', type = argparse.FileType('w'), help = 'Output of divergence regions')

args = parser.parse_args()

#global variable
debug = True

#class definition

#function definition

def divergence_region(input, output):

	flag = 0
	first_list = []
	number = 1

	output.write('#Chromsome\tStart\tEnd\tLength(bp)\tFst value\n')
	
	for eachline in input:
		eachline = eachline.strip()
		first_list = eachline.split()
		if flag == 0:
			form_chr_ID = first_list[0]
			start_pos = int(first_list[1])		#the start of divergence regions
			form_chr_pos = int(first_list[1])		#the former postion
			form_chr_Fst = float(first_list[2])	#the former Fst value
			flag = 1
		elif flag == 1:
			if first_list[0] == form_chr_ID:
				#if (int(first_list[1]) - (int(form_chr_pos)+100000)) <= 200000:		#less than 200k between two regions
				if (int(first_list[1]) - (int(form_chr_pos)+100000)) <= 100000:
					form_chr_Fst += float(first_list[2])
					number += 1
					form_chr_pos = int(first_list[1])
				else:
					output.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.format(form_chr_ID, start_pos, form_chr_pos + 100000, form_chr_pos - start_pos + 100000, form_chr_Fst/number))
					number = 1
					form_chr_ID = first_list[0]
					start_pos = int(first_list[1])      #the start of divergence regions
					form_chr_pos = int(first_list[1])       #the former postion
					form_chr_Fst = float(first_list[2])    #the former Fst value
			else:
				output.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.format(form_chr_ID, start_pos, form_chr_pos + 100000, form_chr_pos - start_pos + 100000, form_chr_Fst/number))
				number = 1
				form_chr_ID = first_list[0]
				start_pos = int(first_list[1])      #the start of divergence regions
				form_chr_pos = int(first_list[1])       #the former postion
				form_chr_Fst = float(first_list[2])    #the former Fst value
	output.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.format(form_chr_ID, start_pos, form_chr_pos + 100000, form_chr_pos - start_pos + 100000, form_chr_Fst/number))


if __name__ == "__main__":
	divergence_region(args.i, args.o)
	args.i.close()
	args.o.close()

