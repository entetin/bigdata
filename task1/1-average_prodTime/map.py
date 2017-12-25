#!/usr/bin/env python
# coding=utf-8
import sys

# gets: raw input file
# returns: antiNucleus, eventFile prodTime Pt

for line in sys.stdin:
	fields = line.split(',')

	antiNucleus = fields[0]   # int
	eventFile   = fields[1]   # uint
	prodTime    = fields[10]  # double
	Pt          = fields[11]  # float

	# variables are initially strings, so no casting needed
	print(antiNucleus + ',' + eventFile + ' ' + prodTime + ' ' + Pt)