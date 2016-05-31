import os
import sys
import csv

"""
This script goes through a dir of FINAL_RESULTS.csv files and finds the NC accession numbers that
correspond to specific Genus_species_subspecies titles. The script then creates two new columns
in the csv file (accession of the query and common name of the hit) with the newfound data from
the original results file. The matches are found by matching the hits with 100 percent identity
and adding the query name and hit accession number to the "name_to_accession" and 
"accession_to_name" dicts.
"""

results_path = "/Users/spencerdodd/Documents/Research/Khrapko_Lab/LocalCrossBLAST_Data_Analysis/selected_seqs"
name_to_accession = {}
accession_to_name = {}

def collect_matches(file_path):

	with open(file_path, 'rb') as csv_file:
		row_data = []
		reader = csv.reader(csv_file, delimiter=',')
		for row in reader:
			row_data.append(row)
			if int(float(row[2])) == 100:
				print row[0] + " : " + row[1]
				name_to_accession[row[0]] = row[1]
				accession_to_name[row[1]] = row[0]

		csv_file.close()
		return row_data


def fill_in_phylo_info(file_path, current_row_data):
	with open(file_path, 'wb+') as csv_result_file:
		writer = csv.writer(csv_result_file, delimiter=',')
		for row in current_row_data:
			hit_accession = name_to_accession[row[0]]
			query_name = accession_to_name[row[1]]
			print hit_accession + " : " + query_name
			writer.writerow([row[0], hit_accession, query_name, row[1], row[2], row[3], row[4], row[5]])

		csv_result_file.close()

def fill_results_folder():
	for dir_name in os.listdir(results_path):
		row_data = []
		if dir_name != '.DS_Store':
			print "Filling in phlyo for {}".format(dir_name)
			file_to_fill = results_path + "/" + dir_name + "/FINAL_RESULTS.csv"
			try:
				current_row_data = collect_matches(file_to_fill)
				fill_in_phylo_info(file_to_fill, current_row_data)
			except:
				print "file already sorted or input is not in expected order"
				pass


def main():
	fill_results_folder()
	

if __name__ == "__main__":
	main()













