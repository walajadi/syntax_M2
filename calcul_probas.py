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
			if cat[0] == 'N':
				cat = "N"
			if cat[0] == 'V':
				cat = "V"
			for suffix in suffixes_list :
				if suffix not in tags :
					tags[suffix] = {}
				if word.endswith(suffix) :
					if cat not in tags[suffix] :
						tags[suffix][cat] = 1
					else :
						tags[suffix][cat] += 1

	return tags

lefff_file = r'lefff_5000.ftb4tags'
suffixes_file = r'pertinent_suffixes+s.txt'

TAGS = counts_tag(lefff_file, suffixes_file)
probas = {}

for suff in TAGS :
	probas[suff] = []
	nb_cat = len(TAGS[suff])
	nb_occ_total = 0
	for cat in TAGS[suff] : 
		nb_occ_total += TAGS[suff][cat]
	for cat in TAGS[suff] :
		nb_occ = TAGS[suff][cat]
		seuil = nb_occ / nb_cat
		if seuil >= 3 :
			proba = float(nb_occ) / nb_occ_total
			proba_str = "%s : %.2f" % (cat, proba)
			probas[suff].append(proba_str)
	
cat_probas = codecs.open(r'cat_probas.txt', "w", "utf-8")

for suff in probas:
	if len(probas[suff]) > 0 :
		probas_str = ""
		for cat in probas[suff] :
			probas_str += cat
			probas_str += "; "
		cat_probas.write(suff+"\t"+probas_str+"\n")
