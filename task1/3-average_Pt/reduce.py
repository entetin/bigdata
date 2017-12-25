#!/usr/bin/env python
# coding=utf-8
import sys

# gets: antiNucleus, Pt
# returns: antiNucleus, float

def do_reduce(key, values):
	'''Returns average value for key.'''
	if len(values) == 0:
		average = 0
	else:
		average = sum(values)/len(values)
	return key, average

prev_key = None
values = []

for line in sys.stdin:

	if len(line) > 2:     # prevent processing of empty lines

		# split line by comma, ignoring the \n
		elems = line.replace('\n', '').replace('\t', '').split(',')

		if len(elems) > 1:

			key   = elems[0]  # antiNucleus
			value = elems[1]  # Pt

			# assuming we get sorted input

			# case: current key is new, and is not first
			if key != prev_key and prev_key is not None:
				# perform reduce on previous key and accumulated values
				result_key, result_value = do_reduce(prev_key, values)
				print(result_key + ',' + str(result_value))
				# clear values for new key
				values = []

			prev_key = key
			values.append(float(value))

# finished reading input, and it was not empty
if prev_key is not None:
	# perform reduce on last key
	result_key, result_value = do_reduce(prev_key, values)
	print(result_key + ',' + str(result_value))