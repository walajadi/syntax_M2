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
	analyseur = Analyser(guesser, dict_proba, lex)
	lexique = getLexique(lex)
	outputfile = 'output-g2.txt'
	output = codcs.open('w', 'utf-8')
	with codecs.open(infile, 'w', 'utf-8') as inputFileObj:
		for line in inputFileObj :
			texte = line.split(' ')
			for word in texte :
				if word.startswith('{') : 
					output.write(word+" ")
				else :
					if word in lexique :
						output.write(word+" ")
					else :
						tag = analyseur.getTag(word)
						output.write(word+"/"+tag[0]+"/"+tag[1])
	inputFileObj.Close()
	