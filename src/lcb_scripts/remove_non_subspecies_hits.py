import os
import sys
import csv
"""
This script removes rows from a set of result data that does not have a subspecies level of
definition in either the query or the hit sequence. It also removes rows that are self-hits. i.e.
hits that are the query sequence (100 percent identity).
"""

# GLOBAL VARS
file_path = "/Users/spencerdodd/Documents/Research/Khrapko_Lab/LocalCrossBLAST_Data_Analysis/PARSED.csv"
save_path = "/Users/spencerdodd/Documents/Research/Khrapko_Lab/LocalCrossBLAST_Data_Analysis/PARSED_COMPLETE.csv"
rows_to_keep = []

def get_data():
	with open(file_path, 'rb') as current_file:
		reader = csv.reader(current_file, delimiter=',')
		for row in reader:
			print row
			if len(row[0].split("_")) > 2 and len(row[2].split("_")) > 2:
				rows_to_keep.append(row)
		current_file.close()

def output_compilation_file():
	print "Writing {} rows to compilation file".format(len(rows_to_keep))
	with open(save_path, 'wb') as save_file:
		writer = csv.writer(save_file, delimiter=',')
		for row in rows_to_keep:
			writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]])


def main():
	get_data()
	output_compilation_file()

if __name__ == "__main__":
	main()











