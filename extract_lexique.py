#-*- coding: utf-8 -*-

import codecs

infile = r"lefff_5000.ftb4tags"
outfile_path = r"lexique.txt"
lexique = []

outfile = codecs.open(outfile_path, "w", "utf-8")
with codecs.open(infile,'r', 'utf-8') as inputFileObj:
	for line in inputFileObj :
		data = line.split('\t')
		word, tag = data[0], data[1]
		lexique.append(word)
		outfile.write(word+"\t"+tag+"\n")
inputFileObj.close()

infile2 = r"lexique_cmpnd_TP.txt"

with codecs.open(infile2,'r', 'utf-8') as inputFileObj:
	for line in inputFileObj :
		if len(line) > 2:
			data = line.split('\t')
			cmpnd, tag = data[0], data[1]
			words = cmpnd.split(' ')
			for word in words :
				if word not in lexique :
					outfile.write(word+"\t"+tag+"\n")
inputFileObj.close()

outfile.close()
