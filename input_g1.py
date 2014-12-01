#-*- coding: utf-8 -*-

def getUnknownWords(infile, lexiqueList) :
	unknowns = []
	with codecs.open(infile, "r", 'utf-8') as inputFileObj:
		for line in inputFileObj:
			words = line.split(' ')#verifier plus tard
			for word in words: 
				if word not in lexiqueList:
					unknowns.append(word)
	return uniknows



