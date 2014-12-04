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

def pondrerLexique(lefff_file, lex_pond):
	counts = {}
	with codecs.open(lefff_file, 'r', 'utf-8') as inputFileObj:
		for line in inputFileObj:
			data = line.split('\t')
			word, tag = data[0], data[1]
			if word not in counts :
				counts[word] = {}
			if tag in counts[word] :
				counts[word][tag] += 1
			else :
				counts[word][tag] = 1
	inputFileObj.close()

	f = codecs.open(lex_pond,'w', 'utf-8')
	for word in counts :
		for tag in counts[word]:
			f.write(word+'\t'+tag+'\t'+str(counts[word][tag])+'\n')
	f.close()

lefff_file = r'lefff_5000.ftb4tags'
suffixes_file = r'sufflist.txt'
lex_pond = r'lexiquePondere.txt'
pondrerLexique(lefff_file, lex_pond)

<<<<<<< HEAD
#TAGS = counts_tag(lefff_file, suffixes_file)
=======
TAGS = counts_tag(lefff_file, suffixes_file)
>>>>>>> b3ff80a3c4067e43994956ed207872d338855f15
