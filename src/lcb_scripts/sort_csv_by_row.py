import csv
import os
import sys

"""
This script sorts a CSV file by a column number (0 based) because Excel's sort is absolute
garbage.
"""
# GLOBAL VARS
import csv
import os
import sys

"""
This script finds all CSV files within a given directory tree and compiles them into a single
CSV file.
"""
# GLOBAL VARS
file_path = "/Users/spencerdodd/Documents/Research/Khrapko_Lab/LocalCrossBLAST/results/prado_debug/COMPILED_RESULTS.csv"
save_path = "/Users/spencerdodd/Documents/Research/Khrapko_Lab/LocalCrossBLAST/results/prado_debug/COMPILED_RESULTS_SORTED.csv"
all_rows = []
column_to_sort_on = 5 # percent difference

def get_rows():
	print "Loading all data into memory"
	with open(file_path, 'rb') as current_file:
		reader = csv.reader(current_file, delimiter=',')
		for row in reader:
			all_rows.append(row)
		current_file.close()

def sort_rows():
	print "Sorting rows by column {}".format(column_to_sort_on)
	all_rows.sort(key=lambda x: x[float(column_to_sort_on)])

def output_compilation_file():
	print "Writing {} rows to compilation file".format(len(all_rows))
	with open(save_path, 'a') as save_file:
		writer = csv.writer(save_file, delimiter=',')
		for row in all_rows:
			print row[0]," "*(30-len(row[0])),row[2]," "*(50-len(row[2])),row[column_to_sort_on]
			writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]])

def delete_problem_data(query_name):
	pass


def main():
	try:
		os.remove(save_path)
	except:
		print 'save_file not created yet'
		pass
	get_rows()
	sort_rows
	output_compilation_file()

if __name__ == "__main__":
	main()










