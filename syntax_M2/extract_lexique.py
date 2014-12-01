#-*- coding: utf-8 -*-

import codecs

infile = r"lefff_5000.ftb4tags"
outfile_path = r"lexique.txt"

outfile = codecs.open(outfile_path, "w", "utf-8")
with codecs.open(infile,'r', 'utf-8') as inputFileObj:
	for line in inputFileObj :
		data = line.split('\t')
		word, tag = data[0], data[1]
		outfile.write(word+"\t"+tag+"\n")
inputFileObj.close()
outfile.close()