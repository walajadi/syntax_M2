#-*- coding: utf-8 -*-

import codecs

infile = r"pertinent_suffixes.txt"
outfile_path = r"pertinent_suffixes+s.txt"
list_suff = []

outfile = codecs.open(outfile_path, "w", "utf-8")
with codecs.open(infile,'r', 'utf-8') as inputFileObj:
	for line in inputFileObj :
		suff = line.strip()
		if suff not in list_suff:
			list_suff.append(suff)
		if suff[-1] != 's':
			new_suff = suff+'s'
			if new_suff not in list_suff:
				list_suff.append(new_suff)
		outfile.write(suff+"\n")
		outfile.write(new_suff+"\n")
inputFileObj.close()

outfile.close()
