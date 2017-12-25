#!/usr/bin/env python
# coding=utf-8
import sys

# gets: antiNucleus, eventFile
# returns: antiNucleus, int

def do_reduce(key, values):
	'''Returns number of unique values for key.'''
	return key, len(set(values))

prev_key = None
values = []

for line in sys.stdin:

	if len(line) > 2:     # prevent processing of empty lines

		# split line by comma, ignoring the \n
		elems = line.strip('\n').split(',')
		key   = elems[0]  # antiNucleus
		value = elems[1]  # eventFile

		# assuming we get sorted input

		# case: current key is new, and is not first
		if key != prev_key and prev_key is not None:
			# perform reduce on previous key and accumulated values
			result_key, result_value = do_reduce(prev_key, values)
			print(result_key + ',' + str(result_value))
			# clear values for new key
			values = []

		prev_key = key
		values.append(value)

# finished reading input, and it was not empty
if prev_key is not None:
	# perform reduce on last key
	result_key, result_value = do_reduce(prev_key, values)
	print(result_key + ',' + str(result_value))