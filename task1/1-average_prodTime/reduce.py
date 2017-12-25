#!/usr/bin/env python
# coding=utf-8
import sys

# gets: antiNucleus, eventFile prodTime Pt
# returns: antiNucleus, eventFile prodTime Pt

def do_reduce(key, values):
	'''Assuming values are [eventFile, prodTime, Pt],
	   return (key, value) if value[1] is greater
	   than average prodTime.'''

	# if there is just one value, pass it
	if len(values) == 1:
		return key, values

	# if there are multiple values, compute average
	second_values = [float(v[1]) for v in values]
	average_second = sum(second_values)/len(second_values)

	# return those that are greater than average
	above_average = []
	for v in values:
		if float(v[1]) > average_second:
			above_average.append(v)

	return key, above_average

prev_key = None
values = []

for line in sys.stdin:

	if len(line) > 2:     # prevent processing of empty lines

		# split line by comma, ignoring the \n
		elems = line.strip('\n').split(', ')
		key   = elems[0]  # antiNucleus
		value = elems[1]  # eventFile prodTime Pt

		value = value.split('  ')  # [eventFile, prodTime, Pt]; two spaces for some reason

		# assuming we get sorted input

		# case: current key is new, and is not first
		if key != prev_key and prev_key is not None:
			# perform reduce on previous key and accumulated values
			result_key, result_values = do_reduce(prev_key, values)
			if len(result_values) > 0:
				for v in result_values:
					if len(v) == 3:
						# we only used v[1] so other elements are still strings
						print(result_key + ',' + v[0] + ' ' + str(v[1]) + ' ' + v[2])
			# clear values for new key
			values = []

		prev_key = key
		values.append(value)

# finished reading input, and it was not empty
if prev_key is not None:
	# perform reduce on last key
	result_key, result_values = do_reduce(prev_key, values)
	if len(result_values) > 0:
		for v in result_values:
			if len(v) == 3:
				print(result_key + ',' + v[0] + ' ' + str(v[1]) + ' ' + v[2])