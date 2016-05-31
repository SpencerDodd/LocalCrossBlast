import glob
import os
import csv
cross_accessions = [
	"NC_014703",
	"NC_013836",
	"NC_016178",
	"NC_018595",
	"NC_013834",
	"NC_007179",
	"NC_006973",
	"NC_006973",
	"NC_006973",
	"NC_006993",
	"NC_013840",
	"NC_013840",
	"NC_007704",
	"NC_007704",
	"NC_007704",
	"NC_013840",
	"NC_014703",
	"NC_018595",
	"NC_016178",
	"NC_006973",
	"NC_013834",
	"NC_006993",
	"NC_007179",
	"NC_013836",
	"NC_013836",
	"NC_014703",
	"NC_016178",
	"NC_018595",
	"NC_013834",
	"NC_007179",
	"NC_013840",
	"NC_013840",
	"NC_006973",
	"NC_006973",
	"NC_006973",
	"NC_006973",
	"NC_006993",
	"NC_006993",
	"NC_006993",
	"NC_006993",
	"NC_006993",
	"NC_007704",
	"NC_007704",
	"NC_013840",
	"NC_014703",
	"NC_007704",
	"NC_018595",
	"NC_016178",
	"NC_013834",
	"NC_013834",
	"NC_006973",
	"NC_006973",
	"NC_006973",
	"NC_007179",
	"NC_006993",
	"NC_006993",
	"NC_006993",
	"NC_006993",
	"NC_006993",
	"NC_013836",
	"NC_006993",
	"NC_006993",
	"NC_006993",
	"NC_006993",
	"NC_006993",
	"NC_006973",
	"NC_006973",
	"NC_006973",
	"NC_006973",
	"NC_007179",
	"NC_007179",
	"NC_007179",
	"NC_016178",
	"NC_016178",
	"NC_018595",
	"NC_018595",
	"NC_013834",
	"NC_013834",
	"NC_013834",
	"NC_014703",
	"NC_013840",
	"NC_013840",
	"NC_013840",
	"NC_013836",
	"NC_013836",
	"NC_007704",
	"NC_013834",
	"NC_016178",
	"NC_018595",
	"NC_006973",
	"NC_006973",
	"NC_006973",
	"NC_006993",
	"NC_006993",
	"NC_006993",
	"NC_006993",
	"NC_006993",
	"NC_006993",
	"NC_007179",
	"NC_014703",
	"NC_013840",
	"NC_013840",
	"NC_013836",
	"NC_007704",
	"NC_007704",
	"NC_016178",
	"NC_018595",
	"NC_013834",
	"NC_006973",
	"NC_006973",
	"NC_006973",
	"NC_006973",
	"NC_007179",
	"NC_006993",
	"NC_006993",
	"NC_006993",
	"NC_006993",
	"NC_006993",
	"NC_014703",
	"NC_013840",
	"NC_013840",
	"NC_013836",
	"NC_007704",
	"NC_007704",
	"NC_018595",
	"NC_016178",
	"NC_013834",
	"NC_006973",
	"NC_006973",
	"NC_006973",
	"NC_006973",
	"NC_007179",
	"NC_006993",
	"NC_006993",
	"NC_006993",
	"NC_006993",
	"NC_006993",
	"NC_014703",
	"NC_013840",
	"NC_013840",
	"NC_013836",
	"NC_007704",
	"NC_007704",
	"NC_007179",
	"NC_006973",
	"NC_006973",
	"NC_006973",
	"NC_006973",
	"NC_006993",
	"NC_006993",
	"NC_006993",
	"NC_006993",
	"NC_006993",
	"NC_016178",
	"NC_018595",
	"NC_013834",
	"NC_014703",
	"NC_013840",
	"NC_013840",
	"NC_013836",
	"NC_007704",
	"NC_007704",
	"NC_006973",
	"NC_006973",
	"NC_006973",
	"NC_006973",
	"NC_006973",
	"NC_006993",
	"NC_006993",
	"NC_006993",
	"NC_006993",
	"NC_006993",
	"NC_006993",
	"NC_006993",
	"NC_007179",
	"NC_007179",
	"NC_007179",
	"NC_007179",
	"NC_016178",
	"NC_016178",
	"NC_016178",
	"NC_016178",
	"NC_018595",
	"NC_018595",
	"NC_018595",
	"NC_018595",
	"NC_013834",
	"NC_013834",
	"NC_013834",
	"NC_014703",
	"NC_014703",
	"NC_014703",
	"NC_013840",
	"NC_013840",
	"NC_013840",
	"NC_013836",
	"NC_013836",
	"NC_013836",
	"NC_013836",
	"NC_007704",
	"NC_007704",
	"NC_006973",
	"NC_006973",
	"NC_006973",
	"NC_006973",
	"NC_006973",
	"NC_006993",
	"NC_006993",
	"NC_006993",
	"NC_006993",
	"NC_006993",
	"NC_006993",
	"NC_006993",
	"NC_007179",
	"NC_007179",
	"NC_007179",
	"NC_007179",
	"NC_016178",
	"NC_016178",
	"NC_016178",
	"NC_016178",
	"NC_018595",
	"NC_018595",
	"NC_018595",
	"NC_018595",
	"NC_013834",
	"NC_013834",
	"NC_013834",
	"NC_014703",
	"NC_014703",
	"NC_014703",
	"NC_013840",
	"NC_013840",
	"NC_013840",
	"NC_013836",
	"NC_013836",
	"NC_013836",
	"NC_013836",
	"NC_007704",
	"NC_007704"
]

file_path = "/Users/spencerdodd/Desktop/test"

def parse_relevant_genus_sequences(file_path):
		# INPUT
		# self.results_dir
		# self.cross_accessions

		# OUTPUT
		# csv in results dir with all relevant results
		result_files = []

		result_rows = []

		print os.getcwd()

		search_term = file_path + "/*.csv"

		for r_file in glob.glob(search_term):

			# check if file is CSV
			# read file
			# write results that have one of the self.cross_accessions into
			# ---- new results file (FINAL RESULTS)
			# process the results
			with open(r_file, "rb") as csvfile:
				
				result_reader = csv.reader(csvfile, delimiter=',')

				for row in result_reader:

					if len(row) > 1:

						hit_accession = row[1]

						for acc in cross_accessions:

							if hit_accession == acc:

								result_rows.append(row)


		# save the results to a new file

		# save the results to a new file

		final_csv_path = file_path + "/FINAL_RESULTS.csv"

		with open(final_csv_path, 'wb') as final_csv:

			c = csv.writer(final_csv, delimiter=',')

			for row in result_rows:

				if int(row[5]) > 13500:

					c.writerow([row[0],row[1],row[2],row[3],row[5],row[4]])

			final_csv.close()








parse_relevant_genus_sequences(file_path)