#-*- coding: utf-8 -*-
from count_tags import TAGS
from input_g1 import getUnknownWords
import codecs

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

class SuffixGuesser :
	#class reconnaisant les suffixes

	def __init__(self, suffixes_file) :
		self.suffixes = []
		with codecs.open(suffixes_file, 'r', 'utf-8') as inputfile :
			for line in inputfile :
				self.suffixes.append(line.rstrip('\n\r'))

		inputfile.close()

		def listeSuffPossibles(self, mot) :
			#on aura une liste possible de suffixes pour un mot donné
			results = set([])
			for suff in self.suffixes :
				if word.endswith(suff) :
					results.append(suff)


			return results

def Analyser :
	
	#analyse morphologique

	def __init__(self, suffReco, probaSuff) :
		self.suff_guesser = SuffixGuesser()
		self.proba_suffix = probaSuff



