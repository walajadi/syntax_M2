#-*- coding: utf-8 -*-


import codecs

infile = r"cat_probas.txt"

def dict_probas(proba_file) :

	probas = {}
	with codecs.open(proba_file,'r', 'utf-8') as inputFileObj :
		for line in inputFileObj:
			cat_dict = {}
			data = line.split('\t')
			suff = data[0]
			cats = data[1].split('; ')
			cats = cats[:-1]
			for cat in cats:
				c = cat.split(' : ')
				pos = c[0]
				prob = c[1]
				cat_dict[pos] = prob;
			sorted_cats = sorted(cat_dict.values())
			print sorted_cats
	inputFileObj.close()

cat_dict = dict_probas(infile)
