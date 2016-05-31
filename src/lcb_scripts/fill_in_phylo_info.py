import os
import sys
import csv

"""
This script goes through a FINAL_RESULTS.csv file and finds the NC accession numbers that
correspond to specific Genus_species_subspecies titles. The script then creates two new columns
in the csv file (accession of the query and common name of the hit) with the newfound data from
the original results file. The matches are found by matching the hits with 100 percent identity
and adding the query name and hit accession number to the "name_to_accession" and 
"accession_to_name" dicts.
"""

file_path = "/Users/spencerdodd/Documents/Research/Khrapko_Lab/LocalCrossBLAST_Data_Analysis/test_phylo_fill/FINAL_RESULTS.csv"
save_file_path = "/Users/spencerdodd/Documents/Research/Khrapko_Lab/LocalCrossBLAST_Data_Analysis/test_phylo_fill/FINAL_RESULTS_FIXED.csv"
name_to_accession = {}
accession_to_name = {}
row_data = []

def collect_matches():

	with open(file_path, 'rb') as csv_file:
		reader = csv.reader(csv_file, delimiter=',')
		for row in reader:
			row_data.append(row)
			if int(float(row[2])) == 100:
				print row[0] + " : " + row[1]
				name_to_accession[row[0]] = row[1]
				accession_to_name[row[1]] = row[0]

		csv_file.close()


def fill_in_phylo_info():
	with open(save_file_path, 'wb+') as csv_result_file:
		writer = csv.writer(csv_result_file, delimiter=',')
		for row in row_data:
			hit_accession = name_to_accession[row[0]]
			query_name = accession_to_name[row[1]]
			print hit_accession + " : " + query_name
			writer.writerow([row[0], hit_accession, query_name, row[1], row[2], row[3], row[4], row[5]])

		csv_result_file.close()

def main():
	collect_matches()
	fill_in_phylo_info()

if __name__ == "__main__":
	main()














