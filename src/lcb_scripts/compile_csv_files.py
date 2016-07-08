import csv
import os
import sys

"""
This script finds all CSV files within a given directory tree and compiles them into a single
CSV file.
"""
# GLOBAL VARS
target_path = "/Users/spencerdodd/Documents/Research/Khrapko_Lab/LocalCrossBLAST/results/prado_debug"
file_paths = []
all_rows = []
save_path = "/Users/spencerdodd/Documents/Research/Khrapko_Lab/LocalCrossBLAST/results/prado_debug/COMPILED_RESULTS.csv"
problem_data = [
	'Parastagonospora_nodorum_SN15',
	'Echymipera_rufescens_australis',
	'Campanulotes_bidentatus_compar',
	'Paragonimus_westermani',
	'Paragonimus_westermani_complex_sp._type_1',
	'Candida_albicans_SC5314',
	'Coccomyxa_subellipsoidea_C-169',
	'Komagataella_phaffii_CBS_7435',
	'Aspergillus_nidulans_FGSC_A4',
	'Saccharomyces_cerevisiae_S288c',
	'Rhizophydium_sp._136',
	'Placozoan_sp._BZ2423',
	'Monoblepharella_sp._JEL15',
	'Helicosporidium_sp._ex_Simulium_jonesi',
	'Trebouxiophyceae_sp._MX-AZ01',
	'Microbotryum_cf._violaceum_BFL-2013',
	'Monomastix_sp._OKE-1'
]

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

def output_compilation_file():
	print "Writing {} rows to compilation file".format(len(all_rows))
	with open(save_path, 'a') as save_file:
		writer = csv.writer(save_file, delimiter=',')
		for row in all_rows:
			try:
				if row[0] not in problem_data:
					print row[0]
					writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]])
			except IndexError as ie:
				print '-----------'
				print ie
				print '-----------'
				pass

def delete_problem_data(query_name):
	pass


def main():
	try:
		os.remove(save_path)
	except:
		print 'save_file not created yet'
		pass
	get_files()
	get_rows()
	output_compilation_file()

if __name__ == "__main__":
	main()










