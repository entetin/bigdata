#!/usr/bin/env python
# coding=utf-8
import sys

# gets: antiNucleus, eventFile prodTime Pt
# returns: antiNucleus, Pt

for line in sys.stdin:
	fields = line.split(',')

	antiNucleus = fields[0]       # int
	Pt = fields[1].split(' ')[2]  # float

	print(antiNucleus + ',' + Pt)