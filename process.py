#-*- coding: utf-8 -*-
from count_tags import TAGS
from input_g1 import getUnknownWords

class_reducer = {
	'VS':'V'
	'VIMP':'V'
	'VINF':'V'
	'VPP':'V'
	'VPR':'V'
	'NP':'NP'
	'ADJ':'ADJ'
	'ADV':'ADV'
	'CL':'X'
	'PONCT':'X'
	'P':'X'
	'DET':'X'
	'CLO':'X'
	'CC':'X'
	'PROWH':'X'
	'PROREL':'X'
}

UNK = getUnknownWords(f1,f2)

'''
	# couper les terminaisons
	# comparer selon le lexique
	# à faire: "unkWord" : 'suffix1' : tagX, 'suffix2' : 'tagY' ...
				on calcule le seuil pour décider !
					si seuil > 3 :
						on décide que c'est pertinent ! 

'''
