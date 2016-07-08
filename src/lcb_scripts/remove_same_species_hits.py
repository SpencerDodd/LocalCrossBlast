import os
import csv

"""
This script removes hits from the results CSV file that contain hits that compare two seqs
of the same species. This is to establish a lower boundary of this within the genus query
that excludes hits in the species query.
"""

# GLOBAL VARS
file_path = "/Users/spencerdodd/Desktop/genus/PARSED_COMPLETE.csv"
save_path = "/Users/spencerdodd/Desktop/genus/PARSED_NO_SPECIES_HITS.csv"
rows_to_keep = []

def get_data():
	with open(file_path, 'rb') as current_file:
		reader = csv.reader(current_file, delimiter=',')
		for row in reader:
			print row
			if row[0].split("_")[1] != row[2].split("_")[1]:
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











