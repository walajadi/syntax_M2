#-*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import sys
import codecs
from lib2.probas2dict import dict_probas


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

		pattern = '^'+stem+'\w?$'
		if re.search('(c|ç)$', stem) != None :
			pattern = '^'+stem[:-1]+'(c|ç|que|ch)\w?$'
		if re.search('ch$', stem) != None :
			pattern = '^'+stem[:-2]+'(c|ç|que|ch)\w?$'
		if re.search('que$', stem) != None :
			pattern = '^'+stem[:-3]+'(c|ç|que|ch)\w?$'
		if re.search('(al|el)$', stem) != None :
			pattern = '^'+stem[:-2]+'(al|el)\w?$'
		if stem[-1] == stem[-2] :
			pattern = '^'+stem+'?\w?$'
		
		for word in self.lexique:
			if re.search(pattern, word) != None :
				return True
			
		return False

	def checkStem(self, token) :

		suffixes = self.aff_guesser.listeSuffPossibles(token)
		prefixes = self.aff_guesser.listePrefPossibles(token)
		stem = token
		suffixes = sorted(suffixes,key=len, reverse = True)
		
		if '-' in stem:
			composes = stem.split('-')
			p1 = composes[0]
			p2 = composes[-1]
			if p1 not in prefixes and p2 not in suffixes:
				if p1 in lexique:
					if p2 in lexique:
						return (token,stem,None,True)
					else:
						for suff in suffixes:
							stemp2 = p2[:len(token) - len(suff)]
							if(len(stemp2) > 2):
								if self.searchLexique(stemp2) :
									return (token, p1+'-'+stemp2, suff, True)
		if len(suffixes) < 1:
			return (token,stem,'',False)
		for suff in  suffixes:
			stem = token[:len(token) - len(suff)]
			if(len(stem) > 2):
				while stem[-1] in "-_":
					stem = stem[:-1]
			if(len(stem) > 2):
				if self.searchLexique(stem) :
					return (token, stem, suff, True)
				else :
					for pref in prefixes :
						stem = token[len(pref):len(token) - len(suff)]
						if(len(stem) > 2):
							while stem[0] in "-_":
								stem = stem[1:]
						if(len(stem)>2):
							if self.searchLexique(stem) :
								return (token, stem,suff,True)
							else:
								stem = token[:len(token) - len(suff)]
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

def getLexique(infile) :
	liste = []
	with codecs.open(infile, 'r', 'utf-8') as inputFileObj:
		for line in inputFileObj :
			data = line.split('\t')
			mot = data[0]
			mot = mot.lower()
			liste.append(mot)
	inputFileObj.close()
	return liste
				
def readFileG1(line, analyseur, lexique) :
	#outputfile = 'output-g2.txt'
	#output = codecs.open(outputfile, 'w', 'utf-8')
	texte = line.split(' ')
	i = 0
	couples = []
	while i < len(texte)-1:
		if texte[i].startswith('{'):
			couple = (texte[i],texte[i+1])
			i += 2
			couples.append(couple)
		else:
			i += 1
			
	if texte[-1].startswith('{'):
		couple = (texte[-1],)
		couples.append(couple)
		
	for c in couples:
		if len(c) > 1 :
			acol = c[0]
			mot = c[1]
			word2search = mot
			word2search = word2search.lower()
			if word2search in lexique :
				print(acol+" "+mot+" ").encode("utf-8"),
			elif mot[0] == '_':
				print(acol+" "+mot+" ").encode("utf-8"),
			elif mot[0] in '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~':
				print(acol+" "+mot+" ").encode("utf-8"),
			else :
				new_acol = acol[:-1]
				(stem, tags, found) = analyseur.getTag(word2search)
				new_acol += "|2:stem:"
				new_acol += stem
				count_tags = 1
				for t in tags :
					pos = t[0]
					cert = t[1]
					new_acol += "|2:tag_"
					new_acol += str(count_tags)
					new_acol += ":"
					new_acol += pos
					new_acol += "|2:certitude_"
					new_acol += str(count_tags)
					new_acol += ":"
					new_acol += cert
					count_tags += 1
					
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
					new_acol += "|2:faute:1"
				else:
					new_acol += "|2:faute:0"
				new_acol += "}"	
				print(new_acol+" "+mot+"\n").encode("utf-8"),
		else:
			print(c[0]+" ").encode("utf-8"),
	
	print("\n")	

			
if __name__ == '__main__':

	suff = r'lib2/pertinent_suffixes+s.txt'
	pref = r'lib2/pertinent_prefixes.txt'
	lex_path = r'lib2/lexique.txt'
	probas_file = r'lib2/cat_probas.txt'
	
	lexique =  getLexique(lex_path)
	dict_proba = dict_probas(probas_file)
	guesser = AffixGuesser(suff, pref)
	analyseur = Analyser(guesser, dict_proba , lexique)

	for line in sys.stdin:
		if (not isinstance(line, unicode)) :
			line = line.decode('utf-8').rstrip("\n\r")
		readFileG1(line, analyseur, lexique)

