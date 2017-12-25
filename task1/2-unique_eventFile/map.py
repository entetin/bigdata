#!/usr/bin/env python
# coding=utf-8
import sys

# gets: antiNucleus, eventFile prodTime Pt
# returns: antiNucleus, eventFile

for line in sys.stdin:
	fields = line.split(',')

	antiNucleus = fields[0]                # int
	eventFile   = fields[1].split(' ')[0]  # uint

	print(antiNucleus + ',' + eventFile)