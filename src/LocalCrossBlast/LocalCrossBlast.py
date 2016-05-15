__author__ = "Spencer Dodd"

import sys
print sys.path

from FastaFileRequest import FastaFileRequest
from FastaStringRequest import FastaStringRequest
from BlastQuery import BlastQuery
import os
import datetime
from Bio import Entrez
from Bio import SeqIO
import glob
import csv

Entrez.email = "dodd.s@husky.neu.edu"

# GLOBAL VARIABLES
global run_time, run_year, run_month, run_day, run_hour, run_minute, run_second
run_time = datetime.datetime.today()
run_year = run_time.year
run_month = run_time.month
run_day = run_time.day
run_hour = run_time.hour
run_minute = run_time.minute
run_second = run_time.second


"""
Represents the main control class for performing a local Cross Blast. Contains
the location of the local database, the file system heirarchy for file reading
and output, and is the source-point for creating and performing queries with
requests.
"""


class LocalCrossBlast:
	def __init__(self):

		self.program_root_dir = self.one_directory_back(os.getcwd())
		self.results_dir = self.program_root_dir + "results/Run_at_{0}hour_{1}min_{2}sec_on_{3}_{4}_{5}/".format(run_hour, run_minute, run_second, run_year, run_month, run_day)
		self.temp_save_path = self.results_dir + "genus_fasta_seqs/"
		self.query_database = None
		self.initial_query = None
		self.initial_query_result_path = None
		self.initial_results_to_cross = []
		self.cross_queries = []
		self.cross_gids = []
		self.cross_accessions = []

		# make dirs that have not been created that the program requires
		self.make_dir(self.results_dir)
		self.make_dir(self.temp_save_path)

	# ------------------------------- METHODS ---------------------------------
	"""
	Creates a new fasta file request and query object and stores it in this
	object's fields
	"""

	def create_fasta_file_cross_blast(self, new_request):

		# create the query
		new_query = BlastQuery(new_request)

		# add it as the crossblast's intial query
		if self.initial_query is None:

			self.initial_query = new_query

			# change the query db type to this query's db type
			self.query_database = new_query.get_database()

		else:

			raise Exception("Initial query is not empty (for some reason)")

	"""
	Creates a new FASTA string request and query object and stores it in
	this object's cross_queries field
	"""

	"""
	Queries the blast server for the initial query results and saves the
	results in a CSV file. Also saves the initial result save path in the
	LocalCrossBlast's field.
	"""

	def perform_initial_query(self):

		if self.initial_query is not None:
			self.initial_query.query_blast_server()
			self.initial_query_result_path = self.initial_query.save_query_results(
				self.results_dir, 'initial')

			print "initial results at: {0}".format(
				self.initial_query_result_path)

	"""
	Sorts through the sequences in the initial results file and determines
	which sequences are related at a genus level of relation to the query
	through terminal input.
	"""

	def add_initial_genus_phylogenetic_info(self):

		print "Getting genus phylogentic info ..."  # for line in results

		query_accession_number = self.initial_query.blast_results_array[0][0].split("ref")[1]
		query_handle = Entrez.efetch(db="nucleotide", id=query_accession_number, rettype="gb", retmode="text")
		query_x = SeqIO.read(query_handle, 'genbank')
		query_name = query_x.annotations['organism']

		for index, result in enumerate(self.initial_query.blast_results_array):

			try:
				hit_accession_number = result[1]
				hit_handle = Entrez.efetch(db="nucleotide", id=hit_accession_number, rettype="gb", retmode="text")
				hit_x = SeqIO.read(hit_handle, 'genbank')
				hit_name = hit_x.annotations['organism']
				hit_seq = result[4]
				hit_seq_length = len(result[4])

				query_genus = query_name.split(" ")[0]
				hit_genus = hit_name.split(" ")[0]

				num_of_hits = len(self.initial_query.blast_results_array)
				percent_complete = (index * 1.0 / num_of_hits * 100)

				print "comparing: {0} | {1} {2}{3}/{4} {5}%".format(query_genus, hit_genus, " "*(50 - (len(query_genus) + len(hit_genus))), index,num_of_hits, percent_complete)

				if query_genus == hit_genus and hit_seq_length > 15000:
					print "Adding relation: {0} | {1}".format(query_name, hit_name)
					self.initial_results_to_cross.append([hit_name, hit_seq])
					self.cross_gids.append(result[2])
					self.cross_accessions.append(result[1])

					# TODO TODO TODO TODO
					# fix so that cross blasts work off of a gilist compiled
					# by the self.cross_gids that is built in this step

					# potential option is as follows
					#	- compile list of GIDs into a txt file in .../bin/blastn
					#	- blastdb_aliastool -gilist XXXXXXXX.gi_list.txt -db refseq_genomic -out refseq_query_db -title refseq_query_db
					#	- use ^^^ database for crossblasting
					# PROBLEMS ^^^^: Segmentation Fault: 11 on aliastool db creation
					#	- additionally, gi_list.txt needs to be in /bin/..kind of
					#		annoying

					# another potential fix:
					#	remove unwanted sequences from the results file before
					#	performing analysis
					# TODO TODO TODO TODO
			except:

				print "Connection error: Retrying ..."


	"""
	Creates queries for each of the initial blast query results. This is the
	cross-blasting section of the blast.
	"""


	def cross_blast_results(self):
		print "CrossBLAST'ing results"

		self.add_initial_genus_phylogenetic_info()

		for query in self.initial_results_to_cross:

			query_name = query[0].replace(" ", "_")
			query_seq = query[1]

			current_query_request = FastaStringRequest(query_name, "blastn", self.query_database,
							   query_sequence=query_seq, save_path=self.temp_save_path)

			current_query = BlastQuery(current_query_request)
			self.cross_queries.append(current_query)

		for cross_query in self.cross_queries:

			print "BLAST'ing {0}".format(cross_query.blast_request.query_name)

			cross_query.query_blast_server()
			cross_query.save_query_results(self.results_dir, 'cross')


	"""
	As the CrossBlast currently cannot be performed on just the relevant
	sequences (at the genus level), we will be removing all sequences that are
	not of the GIDs stored in self.cross_gids from the results.
	"""


	def parse_relevant_genus_sequences(self):
		# INPUT
		# self.results_dir
		# self.cross_accessions

		# OUTPUT
		# csv in results dir with all relevant results

		result_rows = []
		search_term = self.results_dir + "/*.csv"

		for r_file in glob.glob(search_term):

			# check if file is CSV
			# read file
			# write results that have one of the self.cross_accessions into
			# ---- new results file (FINAL RESULTS)
			# process the results
			with open(r_file, "rb") as csvfile:

				result_reader = csv.reader(csvfile, delimiter=',')

				for row in result_reader:

					hit_accession = row[1]

					for acc in self.cross_accessions:

						if hit_accession == acc:

							result_rows.append(row)


		# save the results to a new file

		final_csv_path = self.results_dir + "/FINAL_RESULTS.csv"

		with open(final_csv_path, 'wb') as final_csv:

			c = csv.writer(final_csv, delimiter=',')

			for row in result_rows:

				if row[5] > 13500:

					c.writerow([row[0],row[1],row[2],row[3],row[5],row[4]])

			final_csv.close()



	# --------------------------- HELPER METHODS ------------------------------
	#

	"""
	Creates a given directory in the file system if it doesn't exist
	"""


	def make_dir(self, dir_to_make):
		if not os.path.exists(dir_to_make):
			print "Creating directory {0}".format(dir_to_make)

			os.makedirs(dir_to_make)


	"""
	Returns the pwd, minus one level of depth
	"""


	def one_directory_back(self, current_directory):
		rev_dir = current_directory[::-1]
		rev_result = ''
		result = ''

		for c in rev_dir:
			if c == '/':
				rev_result += rev_dir[rev_dir.index(c):]
				result = rev_result[::-1]

				return result
