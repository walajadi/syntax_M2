#-*- coding: utf-8 -*-

import operator
import codecs
from operator import itemgetter

infile = r"cat_probas.txt"

def dict_probas(proba_file) :

	probas = {}
	with codecs.open(proba_file,'r', 'utf-8') as inputFileObj :
		for line in inputFileObj:
			cat_tuples = []
			data = line.split('\t')
			suff = data[0]
			cats = data[1].split('; ')
			cats = cats[:-1]
			for cat in cats:
				c = cat.split(' : ')
				pos = c[0]
				prob = c[1]
				cat_tuples.append((pos,prob))
			sorted_cats = sorted(cat_tuples, key=itemgetter(1), reverse=True)
			max_value = float(sorted_cats[0][1])
			new_cats = []
			for t in sorted_cats :
				if float(t[1]) > (max_value - 0.25) :
					new_cats.append(t)
			probas[suff] = new_cats
		
	inputFileObj.close()
	return probas

cat_dict = dict_probas(infile)
