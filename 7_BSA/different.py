#!~/bin/python3
#ecoding = utf-8
#This progrem in used to identify differences in parental SNPS
import sys
import re
import os

file1 = open(sys.argv[1],'r')
file2 = open(sys.argv[2],'r')
file3 = open(sys.argv[3],'r')
file4 = open(sys.argv[4],'r')
file5 = open(sys.argv[5],'w')

header = 'CHROM\tPOS\tREF\tALT\tQUAL\tDP\tDP4\tMQ\twild_index\tEMS_index\tdelta_index\n'
file5.write("{0}".format(header))

dict1 = {} #Wild-type parent
list1 = []
list1_7 = []
DP4_min1 = []
for eachline in file1:
	eachline = eachline.strip()
	list1 = eachline.split('\t')
	if '#' in eachline or 'INDEL' in eachline :
		continue
	else:
		if list1[4] == '.':
			list1[4] = list1[3]
		list1_7 = re.split('=|;',list1[7])
		for i in range(0,len(list1_7),2):
			if list1_7[i] == 'DP4':
				DP4_min1 = re.split(',',list1_7[i+1])
				if (float(DP4_min1[0])+float(DP4_min1[1])+float(DP4_min1[2])+float(DP4_min1[3])) != 0:
					SNPindex1 = (float(DP4_min1[2])+float(DP4_min1[3]))/(float(DP4_min1[0])+float(DP4_min1[1])+float(DP4_min1[2])+float(DP4_min1[3]))
					dict1[list1[1]] = [list1[3]]
					dict1[list1[1]].append(list1[4])
					dict1[list1[1]].append(list1[5])
					for i in range(0,len(list1_7),2):
						if list1_7[i] == 'DP':
							dict1[list1[1]].append(list1_7[i+1])
						if list1_7[i] == 'DP4':
							dict1[list1[1]].append(list1_7[i+1])
							dict1[list1[1]].append(SNPindex1)
						if list1_7[i] == 'MQ':
							dict1[list1[1]].append(list1_7[i+1])
#print(dict1)


dict2 = {} #EMS mutant parent
list2 = []
list2_7 = []
DP4_min2 = []
for eachline in file2:
	eachline = eachline.strip()
	list2 = eachline.split('\t')
	flag2 = 0
	if '#' in eachline or 'INDEL' in eachline:
		continue
	if list2[1] in dict1.keys():
		if list2[4] == '.':
			list2[4] = list2[3]
		list2_7 = re.split('=|;',list2[7])
		for i in range(0,len(list2_7),2):
			if list2_7[i] == 'DP4':
				DP4_min2 = re.split(',',list2_7[i+1])
				if (float(DP4_min2[0])+float(DP4_min2[1])+float(DP4_min2[2])+float(DP4_min2[3])) != 0:
					SNPindex2 = (float(DP4_min2[2])+float(DP4_min2[3]))/(float(DP4_min2[0])+float(DP4_min2[1])+float(DP4_min2[2])+float(DP4_min2[3]))
					if float(dict1[list2[1]][2]) >= 20 and float(list2[5]) >= 20: #The base quality of both parents
						if (float(dict1[list2[1]][5]) >= 0.8 and float(SNPindex2) <= 0.2) or (float(dict1[list2[1]][5]) <= 0.2 and float(SNPindex2) >= 0.8): #To extract the parental homozygous locus
							for i in range(0,len(list2_7),2):
								if list2_7[i] == 'DP' and float(dict1[list2[1]][3]) >= 2 and float(list2_7[i+1]) >= 2: #Coverage limits
									flag2 = 0
									DP2 = list2_7[i+1]
									flag2 += 1
								if list2_7[i] == 'DP4':
									DP4_2 = list2_7[i+1]
									flag2 += 1
								if list2_7[i] == 'MQ' and float(dict1[list2[1]][6]) >= 30 and float(list2_7[i+1]) >= 30: #
									MQ2 = list2_7[i+1]
									flag2 += 1
							if flag2 == 3:
								dict2[list2[1]] = [list2[3]] #ref
								dict2[list2[1]].append(list2[4]) #alt
								dict2[list2[1]].append(list2[5])
								dict2[list2[1]].append(DP2)
								dict2[list2[1]].append(DP4_2)
								dict2[list2[1]].append(SNPindex2)
								dict2[list2[1]].append(MQ2)
								#print(dict2)

dict3 = {} #Wild type progeny
list3 = []
list3_7 = []
DP4_min3 = []
for eachline in file3:
	eachline = eachline.strip()
	list3 = eachline.split('\t')
	if '#' in eachline or 'INDEL' in eachline:
		continue
	if list3[1] in dict2.keys():
		if list3[4] == '.':
			list3[4] = list3[3]
		list3_7 = re.split('=|;',list3[7])
		for i in range(0,len(list3_7),2):
			if list3_7[i] == 'DP4':
				DP4_min3 = re.split(',',list3_7[i+1])
				if (float(DP4_min3[0])+float(DP4_min3[1])+float(DP4_min3[2])+float(DP4_min3[3])) != 0:
					if float(dict1[list3[1]][5]) >= 0.8 and float(dict2[list3[1]][5]) <= 0.2:
						SNPindex3 = (float(DP4_min3[0])+float(DP4_min3[1]))/(float(DP4_min3[0])+float(DP4_min3[1])+float(DP4_min3[2])+float(DP4_min3[3]))
					if float(dict1[list3[1]][5]) <= 0.2 and float(dict2[list3[1]][5]) >= 0.8:
						SNPindex3 = (float(DP4_min3[2])+float(DP4_min3[3]))/(float(DP4_min3[0])+float(DP4_min3[1])+float(DP4_min3[2])+float(DP4_min3[3]))
					dict3[list3[1]] = [list3[3]]
					dict3[list3[1]].append(list3[4])
					dict3[list3[1]].append(list3[5])
					for i in range(0,len(list3_7),2):
						if list3_7[i] == 'DP':
							dict3[list3[1]].append(list3_7[i+1])
						if list3_7[i] == 'DP4':
							dict3[list3[1]].append(list3_7[i+1])
							dict3[list3[1]].append(SNPindex3)
						if list3_7[i] == 'MQ':
							dict3[list3[1]].append(list3_7[i+1])
	#						print(dict3)

dict4 = {} #EMS mutant progeny
list4 = []
list4_7 = []
DP4_min4 = []
for eachline in file4:
	eachline = eachline.strip()
	list4 = eachline.split('\t')
	flag4 = 0
	if '#' in eachline or 'INDEL' in eachline:
		continue
	if list4[4] == '.':
		list4[4] = list4[3]
	if list4[1] in dict3.keys():
		list4_7 = re.split('=|;',list4[7])
		for i in range(0,len(list4_7),2):
			if list4_7[i] == 'DP4':
				DP4_min4 = re.split(',',list4_7[i+1])
				if (float(DP4_min4[0])+float(DP4_min4[1])+float(DP4_min4[2])+float(DP4_min4[3])) != 0:
					if float(dict1[list4[1]][5]) >= 0.8 and float(dict2[list4[1]][5]) <= 0.2:
						SNPindex4 = (float(DP4_min4[0])+float(DP4_min4[1]))/(float(DP4_min4[0])+float(DP4_min4[1])+float(DP4_min4[2])+float(DP4_min4[3]))
					if float(dict1[list4[1]][5]) <= 0.2 and float(dict2[list4[1]][5]) >= 0.8:
						SNPindex4 = (float(DP4_min4[2])+float(DP4_min4[3]))/(float(DP4_min4[0])+float(DP4_min4[1])+float(DP4_min4[2])+float(DP4_min4[3]))
					if float(dict3[list4[1]][2]) >= 20 and float(list4[5]) >= 20:
						for i in range(0,len(list4_7),2):
							if list4_7[i] == 'DP' and float(dict3[list4[1]][3]) >= 2 and float(list4_7[i+1]) >= 2:
								DP4 = list4_7[i+1]
								flag4 += 1
							if list4_7[i] == 'DP4':
								DP4_4 = list4_7[i+1]
								flag4 += 1
							if list4_7[i] == 'MQ' and float(dict3[list4[1]][6]) >= 30 and float(list4_7[i+1]) >= 30:
								MQ4 = list4_7[i+1]
								flag4 += 1
						if flag4 == 3:
							file5.write('{0}\t{1}\t{2}\t{3}/{4}/{5}/{6}\t{7}/{8}/{9}/{10}\t{11}/{12}/{13}/{14}\t{15}/{16}/{17}/{18}\t{19}/{20}/{21}/{22}\t{23}\t{24}\t{25}\n'.format(list4[0],list4[1],list4[3],dict1[list4[1]][1],dict2[list4[1]][1],dict3[list4[1]][1],list4[4],dict1[list4[1]][2],dict2[list4[1]][2],dict3[list4[1]][2],list4[5],dict1[list4[1]][3],dict2[list4[1]][3],dict3[list4[1]][3],DP4,dict1[list4[1]][4],dict2[list4[1]][4],dict3[list4[1]][4],DP4_4,dict1[list4[1]][6],dict2[list4[1]][6],dict3[list4[1]][6],MQ4,dict3[list4[1]][5],SNPindex4,float(SNPindex4)-float(dict3[list4[1]][5])))

file1.close()
file2.close()
file3.close()
file4.close()
file5.close()
