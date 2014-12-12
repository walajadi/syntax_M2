#-*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import codecs
from input_g1 import getLexique
from input_g1 import readFileG1
from probas2dict import dict_probas
from pprint import pprint

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
		self.probaTags = probaSuff
		self.lexique = lexique
		self.last_suffix = ''

	def scoreToken(self, suff) :
		return self.proba_suffix[suff]
	
	def searchLexique(self, stem) :

		pattern = '^'+stem+'\w{,2}$'
		if re.search('(c|ç)$', stem) != None :
			pattern = '^'+stem[:-1]+'(c|ç|que|ch)\w{,2}$'
		if re.search('ch$', stem) != None :
			pattern = '^'+stem[:-2]+'(c|ç|que|ch)\w{,2}$'
		if re.search('que$', stem) != None :
			pattern = '^'+stem[:-3]+'(c|ç|que|ch)\w{,2}$'
		if re.search('(al|el)$', stem) != None :
			pattern = '^'+stem[:-2]+'(al|el)\w{,2}$'
		if stem[-1] == stem[-2] :
			pattern = '^'+stem+'?.{,2}$'
		
		for word in self.lexique:
			if re.search(pattern, word) != None :
				return True
			
		return False

	def checkStem(self, token) :

		suffixes = self.aff_guesser.listeSuffPossibles(token)
		prefixes = self.aff_guesser.listePrefPossibles(token)
		stem = token
		suffixes = sorted(suffixes,key=len, reverse = True)
		if len(suffixes) < 1:
			return (token,stem,'',False)
		for suff in  suffixes:
			stem = token[:len(token) - len(suff)]
			if(len(stem) > 1):
				if self.searchLexique(stem) :
					#bingo trouvé
					suffix = suff
					return (token, stem, suff, True) #or something like this
				else :
					for pref in prefixes :
						stem = token[len(pref):len(token) - len(suff)]
						if self.searchLexique(stem) :
							return (token, stem,suff,True)#ici on peux retourner le prefixe ??
						#elif self.searchLexique(stem) :
						#	return (token, stem, suff)
		try :
			return (token, stem, suffixes[0], False)
		except KeyError:
			return (token, stem, None, False)

	def getTag(self, token) :
		probasTags = []
		data = self.checkStem(token)
		stem = data[1]
		suff = data[2]
		found = data[3]
		if suff != None:
			try :
				return (stem, self.probaTags[suff], found)
			except KeyError:
				return (stem, [], found)
		else:
			return (stem, [], found)
			
def readFileG1(infile, suff, pref, lex, dict_proba) :
	guesser = AffixGuesser(suff, pref)
	lexique = getLexique(lex)
	analyseur = Analyser(guesser, dict_proba, lexique)
	outputfile = 'output-g2.txt'
	output = codecs.open(outputfile, 'w', 'utf-8')
	with codecs.open(infile, 'r', 'utf-8') as inputFileObj:
		for line in inputFileObj :
			line = line.strip()
			texte = line.split(' ')
			i = 0
			couples = []
			while i < len(texte)-1:
				if texte[i].startswith('{'):
					if not texte[i+1].startswith('{'):
						couple = (texte[i],texte[i+1])
						i += 2
					else:
						couple = (texte[i],)
						i += 1
					couples.append(couple)
			if texte[-1].startswith('{'):
				couple = (texte[-1],)
				couples.append(couple)
			for c in couples:
				if len(c) > 1 : # sinon c'est ponctuation ou entite nommee
					acol = c[0]
					mot = c[1]
					if mot in lexique :
						output.write(acol+" "+mot+" ")
					else :
						new_acol = acol[:-1]
						(stem, tags, found) = analyseur.getTag(mot)
						new_acol += "|2:stem:"
						new_acol += stem
						for t in tags :
							pos = t[0]
							cert = t[1]
							new_acol += "|2:tag:"
							new_acol += pos
							new_acol += "|2:certitude:"
							new_acol += cert
							
						change = ""
						if len(tags) >= 3:
							cats = [tag[0] for tag in tags]
							if 'N' in cats:
								if 'ADJ' in cats:
									if 'V' in cats:
										change = "pratique"
									elif 'ADV' in cats:
										change="mal"
						elif len(tags) == 2:
							cats = [tag[0] for tag in tags]
							if 'N' in cats:
								if 'V' in cats:
									change = "mesure"
								elif 'ADJ' in cats:
									change = "voisin"
								elif 'ADV' in cats:
									change = "ensemble"
							elif 'V' in cats:
								if 'ADJ' in cats:
									change = "complète"
								elif 'ADV' in cats:
									change = "maintenant"
						elif len(tags) == 1:
							pos = tags[0][0]
							prob = float(tags[0][1])
							if prob >= 0.7 :
								if pos == 'N':
									change = "chien"
								elif pos == 'V':
									change = "voit"
								elif pos == 'ADJ':
									change = "exceptionnel"
								elif pos == 'ADV':
									change = "exceptionnellement"
						if change != "":
							new_acol += "|2:change:"
							new_acol += change
						if found == False:
							new_acol += "|2:faute"
						new_acol += "}"	
						output.write(new_acol+" "+mot+"\n")
				else:
					output.write(c[0]+" ")
			
			output.write("\n")	
			'''	
			for word in texte :
				if word.startswith('{') : 
					output.write(word+" ")
				else :
					if word in lexique :
						output.write(word+" ")
					else :
						tag = analyseur.getTag(word)
						output.write(word+"/"+tag[0]+"/"+tag[1])
			'''
	inputFileObj.close()
			
if __name__ == '__main__':

	suff = r'pertinent_suffixes+s.txt'
	pref = r'pertinent_prefixes.txt'
	lex_path = r'lexique.txt'
	probas_file = r'cat_probas.txt'
	lexique =  getLexique(lex_path)
	dict_proba = dict_probas(probas_file)
	#pprint(dict_proba)
	guesser = AffixGuesser(suff, pref)
	#print guesser.listePrefPossibles(u'antinucléaire')
	#print guesser.listeSuffPossibles(u'industrialisation')
	analyseur = Analyser(guesser, dict_proba , lexique)
	#print analyseur.checkStem('anticonsititutionnellement')
	print analyseur.getTag("antisocialisme")
	readFileG1('phrase.txt', 'pertinent_suffixes+s.txt', 'pertinent_prefixes.txt', lex_path, dict_proba)

