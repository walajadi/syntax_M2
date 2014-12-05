#-*- coding: utf-8 -*-
#from count_tags import TAGS
#from input_g1 import getUnknownWords
import codecs
'''
class_reducer = {
	'VS':'V',
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
'''
class AffixGuesser :

	#class reconnaisant les suffixes

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
		return results

	def listePrefPossibles(self, unknownWord) :
		results = set([])
		for pref in self.prefixes:
			if unknownWord.startswith(pref) or unknownWord.startswith(pref+'-') :
				results.add(pref)
		return results



class Analyser :
	
	#analyse morphologique

	def __init__(self, affixGuesser, probaSuff, lexique) :
		
		self.aff_guesser = affixGuesser
		self.proba_suffix = probaSuff
		self.lexique = lexique

	def scoreToken(self, token) :
		pass

	def checkStem(self, token) :

		suffixes = self.affixGuesser.listeSuffPossibles(token)
		prefixes = self.affixGuesser.listePrefPossibles(token)

		for suff in suffixes :
			if token[:len(suff)] in self.lexique :
				#bingo trouvé
				return True #or something like this
			else :
				for pref in prefixes :
					if token[len(pref):] in self.lexique :
						return (token, pref)
					elif token[len(pref):len(suff)] in self.lexique :
						return (token, (pref, suff))
		return (token, null)

 
if __name__ == '__main__':
	suff = r'pertinent_suffixes.txt'
	pref = r'pertinent_prefixes.txt'

	guesser = AffixGuesser(suff, pref)
	print guesser.listePrefPossibles(u'antinucléaire')
	print guesser.listeSuffPossibles(u'industrialisation')