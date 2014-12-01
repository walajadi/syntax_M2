#-*- coding: utf-8 -*-

import codecs
import pprint
def counts_tag(lefff_file, suffixes_file) :
	tags = {}
	suffixes_list = []
	with codecs.open(suffixes_file,'r', 'utf-8') as inputFileObj :
		for line in inputFileObj:
			suffixes_list.append(line.strip())
	inputFileObj.close()

	with codecs.open(lefff_file,'r', 'utf-8') as inputFileObj :
		for line in inputFileObj :
			word, cat  = line.split()[0], line.split()[1]
			for suffix in suffixes_list :
				if suffix not in tags :
					tags[suffix] = {}
				if word.endswith(suffix) :
					if cat not in tags[suffix] :
						tags[suffix][cat] = 1
					else :
						tags[suffix][cat] += 1

	return tags

lefff_file = r'/home/slim/Git/syntax_M2/lefff_5000.ftb4tags'
suffixes_file = r'/home/slim/Git/syntax_M2/sufflist.txt'

TAGS = counts_tag(lefff_file, suffixes_file)