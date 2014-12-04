#!/usr/bin/env python
# -*- coding: utf-8 -*-

cats = {}

f = open('lexique.txt', 'r')

for str in f:
	line = str.split("\t")
	mot = line[0]
	cat = line[1]
	cats[mot] = cats.get(mot,[])
	cats[mot].append(cat)

for m in cats:
	if len(cats[m]) > 1:
		print m, " : ", cats[m], "\n"
