#-*- coding: utf-8 -*-

import codecs
#from process import Analyser, AffixGuesser


def getUnknownWords(infile, lexiqueList) :
	unknowns = []
	with codecs.open(infile, "r", 'utf-8') as inputFileObj:
		for line in inputFileObj:
			words = line.split(' ')#verifier plus tard
			for word in words: 
				if word not in lexiqueList:
					unknowns.append(word)
	return uniknows



def getLexique(infile) :
	liste = []
	with codecs.open(infile, 'r', 'utf-8') as inputFileObj:
		for line in inputFileObj :
			data = line.split('\t')
			liste.append(data[0])
	inputFileObj.close()
	return liste

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
			if len(texte) > 1 : # sinon c'est ponctuation ou entite nommee
				acol = texte[0]
				mot = texte[1]
				if mot in lexique :
					output.write(line+"\n")
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
				output.write(line+"\n")
				
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
