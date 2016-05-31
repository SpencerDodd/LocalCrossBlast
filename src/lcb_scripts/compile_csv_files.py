import csv
import os
import sys

"""
This script finds all CSV files within a given directory tree and compiles them into a single
CSV file.
"""
# GLOBAL VARS
target_path = "/Users/spencerdodd/Documents/Research/Khrapko_Lab/LocalCrossBLAST_Data_Analysis/selected_seqs"
file_paths = []
all_rows = []
save_path = target_path + "/COMPILED_RESULTS.csv"


def get_files():
	for root, dirnames, filenames in os.walk(target_path):
		for file_name in filenames:
			if ".csv" in file_name:
				print 'adding file {}'.format(file_name)
				file_paths.append(os.path.join(root, file_name))


def get_rows():
	for file_path in file_paths:
		if not 'DS_Store' in file_path:
			file_size = os.path.getsize(file_path)
			print "Getting data from {} | {} bytes".format(file_path, file_size)
			if file_size != 0:
				with open(file_path, 'rb') as current_file:
					reader = csv.reader(current_file, delimiter=',')
					for row in reader:
						all_rows.append(row)
					current_file.close()
			else:
				print "File is empty"
				pass

def output_compilation_file():
	with open(save_path, 'wb') as save_file:
		writer = csv.writer(save_file, delimiter=',')
		for row in all_rows:
			writer.writerow(row)


def main():
	get_files()
	get_rows()
	output_compilation_file()

if __name__ == "__main__":
	main()










