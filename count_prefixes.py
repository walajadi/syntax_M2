#-*- coding: utf-8 -*-

import codecs
import pprint
def counts_tag(lefff_file, prefixes_file) :
	tags = {}
	prefixes_list = []
	with codecs.open(prefixes_file,'r', 'utf-8') as inputFileObj :
		for line in inputFileObj:
			prefixes_list.append(line.strip())
	inputFileObj.close()

	with codecs.open(lefff_file,'r', 'utf-8') as inputFileObj :
		for line in inputFileObj :
			word, cat  = line.split()[0], line.split()[1]
			for prefix in prefixes_list :
				if prefix not in tags :
					tags[prefix] = {}
				if word.startswith(prefix) :
					if cat not in tags[prefix] :
						tags[prefix][cat] = 1
					else :
						tags[prefix][cat] += 1

	return tags

lefff_file = r'lefff_5000.ftb4tags'
prefixes_file = r'preflist.txt'

TAGS = counts_tag(lefff_file, prefixes_file)

new_pref_file = codecs.open(r'pertinent_prefixes.txt', "w", "utf-8")

for pref in TAGS:
	if len(TAGS[pref]) > 0 :
		new_pref_file.write(pref+"\n")
		
