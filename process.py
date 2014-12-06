#-*- coding: utf-8 -*-
#from count_tags import TAGS
#from input_g1 import getUnknownWords
import re
import codecs
from input_g1 import getLexique
from probas2dict import dict_probas
class_reducer = {
	'VS':'V',
	'VIMP':'V',
	'VINF':'V',
	'VPP':'V',
	'VPR':'V',
	'NPP':'N',
	'NC' : 'N',
	'ADJ':'ADJ',
	'ADV':'ADV',
}

class AffixGuesser :

	#classe reconnaisant les affixes

	def __init__(self, suffixes_file, prefixes_file) :
		self.suffixes = []
		self.prefixes = []
		with codecs.open(suffixes_file, 'r', 'utf-8') as inputfile :
			for line in inputfile :
				self.suffixes.append(line.rstrip('\n\r'))

		inputfile.close()

		with codecs.open(prefixes_file, 'r', 'utf-8') as inputfile_ :
			for line in inputfile_ :
				self.prefixes.append(line.rstrip('\n\r'))
		
		inputfile_.close()

	def listeSuffPossibles(self, unknownWord) :
		#on aura une liste possible de suffixes pour un mot donné
		results = set([])
		for suff in self.suffixes :
			if unknownWord.endswith(suff) :
				results.add(suff)
		results = sorted(results, key=len, reverse=True)
		return results

	def listePrefPossibles(self, unknownWord) :
		results = set([])
		for pref in self.prefixes:
			if unknownWord.startswith(pref) :
				results.add(pref)
		results = sorted(results, key=len, reverse=True)
		return results



class Analyser :
	
	#analyse morphologique

	def __init__(self, affixGuesser, probaSuff, lexique) :
		
		self.aff_guesser = affixGuesser
		self.proba_suffix = probaSuff
		self.lexique = lexique
		self.last_suffix = ''

	def scoreToken(self, suff) :
		return self.proba_suffix[suff]
	
	def searchLexique(self, stem) :
		pattern = '^'+stem+'.{,2}$'
		if re.search('(c|ç)$', stem) != None :
			pattern = '^'+stem[:-1]+'(c|ç|que|ch).{,2}$'
		if re.search('ch$', stem) != None :
			pattern = '^'+stem[:-2]+'(c|ç|que|ch).{,2}$'
		if re.search('que$', stem) != None :
			pattern = '^'+stem[:-3]+'(c|ç|que|ch).{,2}$'
		if re.search('(al|el)$', stem) != None :
			pattern = '^'+stem[:-2]+'(al|el).{,2}$'
		if stem[-1] == stem[-2] :
			pattern = '^'+stem+'?.{,2}$'
		
		if re.search(pattern, self.lexique) != None :
			return True
		else :
			return False

	def checkStem(self, token) :

		suffixes = self.affix_guesser.listeSuffPossibles(token)
		prefixes = self.affix_guesser.listePrefPossibles(token)
		stem = token

		for suff in sort_truc(suffixes) :
			if searchLexique(token[:len(suff)]) :
				#bingo trouvé
				suffix = suff
				stem = token[:len(suff)]
				return (token, stem, suff) #or something like this
			else :
				for pref in prefixes :
					if searchLexique(token[len(pref):]) :
						return (token, stem, null)
					elif searchLexique(token[len(pref):len(suff)]) :
						return (token, stem, suff)

		return (token, stem, suffixes[0])

 
if __name__ == '__main__':

	suff = r'pertinent_suffixes.txt'
	pref = r'pertinent_prefixes.txt'
	lex_path = r'lexique.txt'
	probas_file = r'cat_probas.txt'
	lexique =  getLexique(lex_path)
	dict_proba = dict_probas(probas_file)
	guesser = AffixGuesser(suff, pref)
	#print guesser.listePrefPossibles(u'antinucléaire')
	#print guesser.listeSuffPossibles(u'industrialisation')
	analyseur = Analyser(guesser, dict_proba , lexique)
