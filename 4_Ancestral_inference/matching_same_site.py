#!python3
#coding=utf-8
#This script is used to calculate overlap percentage between common allel and other population

import re,sys,os

f1=open(sys.argv[1],"r")#common allel
f2=open(sys.argv[2],"r")#Other population allel info
f3=open(sys.argv[3],"w")#percentage file

dict1={}
percen=0

f3.write('Chr\tlocus\tindentity\n')
for eachline1 in f1:
	eachline1 = eachline1.strip()
	list1 = eachline1.split('\t')
	if not eachline1 or eachline1[0] == "#":
		continue
	else:
		dict1[list1[1]]=str(list1[2])

for eachline2 in f2:
	eachline2 = eachline2.strip()
	list2 = eachline2.split('\t')
	list3 = re.split(' ',list2[-1])
	if not eachline2 or eachline2[0] == "#":
		continue
	else:
		if list2[1] in dict1.keys():
			for i in range(0,len(list3)):
				if str(list3[i]) == dict1[list2[1]]:
					percen += 1
			percentage = percen/1	#individual number
			f3.write('{0}\t{1}\t{2}\n'.format(list2[0],list2[1],percentage))
	percen = 0
