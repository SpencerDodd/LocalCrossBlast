__author__ = "Spencer Dodd"

from FastaFileRequest import FastaFileRequest
from FastaStringRequest import FastaStringRequest
from BlastQuery import BlastQuery
import os
import datetime
from Bio import Entrez
from Bio import SeqIO
import glob
import csv
import matplotlib.pyplot as plt
import numpy as np
import traceback
import shutil

Entrez.email = "dodd.s@husky.neu.edu"

# TODO
# 1. change so that if a filename exists in the results directory that contains
# 	the genus of the query, the cross blast is dropped (results already exist)
# 2. add the accession number of the query to the results and the name of
# 	the hit to results

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
		self.base_results_dir = "/root/Research/mito_phylo/Results/genus/" #"/Volumes/Results/genus/"
		self.results_dir = None
		self.temp_save_path = None
		self.query_database = None
		self.initial_query = None
		self.initial_genus = None
		self.initial_name = None
		self.initial_query_result_path = None
		self.initial_results_to_cross = []
		self.cross_queries = []
		self.cross_gids = []
		self.cross_accessions = []
		self.query_accession_number = None
		self.gap_in_hits = 0
		self.mito_size_cutoff = 10000

		# for checking if sequence has already been blasted by this query
		self.saved_sequences = self.base_results_dir + "saved_seqs/used.txt" #"/Volumes/Results/genus/saved_seqs/used.txt"

		# for phylogenetic selection of genus{0} species{1} and subspecies {2}
		self.phylo_check_level = 0

		# for output percentage
		self.genus_lookup_index = 0
		self.genus_hits_to_search = 1
		self.current_cross_query = 0
		self.queries_in_cross = 1
		self.id_number = None

		# for data analysis
		self.genus_distances = []

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

			if self.is_sequence_already_used(self.initial_query.get_query_sequence()):
				raise ValueError("QUERY SEQUENCE HAS ALREADY BEEN USED")

			self.make_initial_dirs(self.initial_query)
			self.initial_query.query_blast_server()
			self.initial_query_result_path = self.initial_query.save_query_results(
				self.results_dir, 'initial')

			print "initial results at: {0}".format(
				self.initial_query_result_path)

		else:

			raise Exception("THERE IS NO INITIAL QUERY")

	# make dirs that have not been created that the program requires
	def make_initial_dirs(self, initial_query):

		self.results_dir = self.base_results_dir + "Run_at_{0}hour_{1}min_{2}sec_on_{3}_{4}_{5}/".format(
			run_hour, run_minute, run_second, run_year, run_month,
			initial_query.get_query_name())

		# TODO TODO TODO TODO
		"""self.program_root_dir + "results/Run_at_{0}hour_{1}min_{2}sec_on_{3}_{4}_{5}/".format(
			run_hour, run_minute, run_second, run_year, run_month,
			initial_query.get_query_name())"""
		self.temp_save_path = self.results_dir + "genus_fasta_seqs/"

		self.make_dir(self.results_dir)
		self.make_dir(self.temp_save_path)

	"""
	Sorts through the sequences in the initial results file and determines
	which sequences are related at a genus level of relation to the query
	through terminal input.
	"""

	def add_initial_genus_phylogenetic_info(self):

		try:

			print "Getting genus phylogentic info ..."  # for line in results
			self.genus_hits_to_search = len(
				self.initial_query.blast_results_array)
			query_first_column = self.initial_query.blast_results_array[0][0]
			self.get_accession_from_sequence_title(query_first_column)

			if self.query_accession_number == "cannot_parse_genus":
				raise Exception("Cannot parse genus.. exiting")

			query_handle = Entrez.efetch(db="nucleotide",
										 id=self.query_accession_number,
										 rettype="gb", retmode="text")
			query_x = SeqIO.read(query_handle, 'genbank')
			query_name = query_x.annotations['organism']
			query_genus = query_name.split(" ")[self.phylo_check_level]

			# save for later (checking if results already exist)
			self.initial_name = query_name
			self.initial_genus = query_genus


		except:
			print "Problem connecting to Entrez. Retrying ..."
			print traceback.print_exc()
			self.add_initial_genus_phylogenetic_info()

		if self.query_already_made():
			# for GUI
			self.set_completion_to_100()
			raise Exception(
				"Query for phylogenetic level already made. Aborting BLAST ...")

		if not self.query_has_subspecies():
			self.set_completion_to_100()
			raise Exception("Query doesn't have subspecies level of definition")

		for index, result in enumerate(self.initial_query.blast_results_array):

			self.genus_lookup_index = index

			if self.gap_in_hits < 20:

				try:
					hit_accession_number = result[1]
					print "HIT ACCESSION : {}".format(hit_accession_number) # DEBUG TODO FOR HTTP ERROR 400 BAD REQUEST
					hit_handle = Entrez.efetch(db="nucleotide",
											   id=hit_accession_number,
											   rettype="gb", retmode="text")
					hit_x = SeqIO.read(hit_handle, 'genbank')
					hit_name = hit_x.annotations['organism']
					hit_seq = result[4]
					hit_seq_length = len(result[4])
					hit_genus = hit_name.split(" ")[self.phylo_check_level]

					num_of_hits = len(self.initial_query.blast_results_array)
					percent_complete = (index * 1.0 / num_of_hits * 100)

					print "comparing: {0} | {1} {2}{3}/{4} {5}%".format(
						query_genus, hit_genus,
						" " * (50 - (len(query_genus) + len(hit_genus))), index,
						num_of_hits, percent_complete)

					if query_genus == hit_genus and hit_seq_length > self.mito_size_cutoff:
						print "Adding relation: {0} | {1}".format(query_name,
																  hit_name)
						self.initial_results_to_cross.append(
							[hit_name, hit_seq])
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

						self.gap_in_hits = 0

					else:

						self.gap_in_hits += 1

				except Exception as e:
					print "Connection error: {} | Retrying ...".format(e)

			else:

				self.genus_lookup_index = self.genus_hits_to_search

	"""
	Returns true if the query does not have a subspecies level of definition
	"""

	def query_has_subspecies(self):

		phylo = self.initial_name.split(" ")
		print phylo
		if len(phylo) < 3:
			return False
		else:
			return True

	"""
	returns true if the query genus already has results in the results directory
	"""

	def query_already_made(self):

		print "Checking if query has already been made"

		results = [x[0] for x in os.walk(self.base_results_dir)]

		self.num_of_genus_hits = 0

		for result in results:
			if self.initial_genus in result and "genus_fasta_seqs" not in result:
				self.num_of_genus_hits += 1
				print "{0} in | query hit: {1}".format(self.initial_genus,
													   result)

		print "number of genus hits for {0}: {1}".format(self.num_of_genus_hits,
														 self.initial_genus)

		if self.num_of_genus_hits > 1:
			"Query has already been made. Exiting BLAST ..."
			return True

		"Query genus is novel. Continuing"
		return False

	"""
	"""

	def get_accession_from_sequence_title(self, query_first_column):

		print "Getting accession from sequence title ..."
		print "sequence title: {}".format(query_first_column)

		if "ref" in query_first_column:
			self.query_accession_number = query_first_column.split("ref")[1]
		elif "emb" in query_first_column:
			self.query_accession_number = query_first_column.split("emb")[1]
		elif "dbj" in query_first_column:
			self.query_accession_number = query_first_column.split("dbj")[1]
		elif "gb" in query_first_column:
			self.query_accession_number = query_first_column.split("gb")[1]
		else:
			self.query_accession_number = "cannot_parse_genus"

		print self.query_accession_number

	"""
	Creates queries for each of the initial blast query results. This is the
	cross-blasting section of the blast.
	"""

	def cross_blast_results(self):
		print "CrossBLAST'ing results"

		self.save_used_sequence(self.initial_query.get_query_sequence())

		self.add_initial_genus_phylogenetic_info()

		self.queries_in_cross = len(self.initial_results_to_cross)

		for query in self.initial_results_to_cross:
			query_name = query[0].replace(" ", "_")
			query_seq = query[1]

			current_query_request = FastaStringRequest(query_name, "blastn",
													   self.query_database,
													   query_sequence=query_seq,
													   save_path=self.temp_save_path)

			current_query = BlastQuery(current_query_request)
			self.cross_queries.append(current_query)

		for index, cross_query in enumerate(self.cross_queries):
			self.current_cross_query = index + 1

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

				if int(row[5]) > 13500:
					c.writerow([row[0], row[1], row[2], row[3], row[5], row[4]])

			final_csv.close()

	"""
	Performs histogram analysis for genus related data
	"""

	def analyze_genus_data(self):

		# if there are genus hits...
		if len(self.genus_distances) > 0:

			final_csv_path = self.results_dir + "/FINAL_RESULTS.csv"

			with open(final_csv_path, "rb") as final_csv_file:
				reader = csv.reader(final_csv_file, delimiter=',')

				for row in reader:
					print row
					self.genus_distances.append(float(row[3]))

			bin_max = 10
			bins = np.linspace(0, bin_max, 200)
			colors = ['dodgerblcolorue']
			plt.hist(self.genus_distances, bins, alpha=0.5,
					 label='{0} (Range: {1} to {2})'.format('Genus', min(
						 self.genus_distances), max(self.genus_distances)))

			plt.ylabel('Frequency')
			plt.xlabel('Percent dist to common ancestor')
			plt.title('Overview')
			plt.legend(loc='upper right')
			plt.savefig(
				'{0}/Overview_{1}.png'.format(self.results_dir,
											  self.get_query_name()))

	def set_completion_to_100(self):

		self.genus_lookup_index = 1
		self.genus_hits_to_search = 1

	"""
	Returns the current progress of the blast for the progress bar
	"""

	def current_progress(self):

		phylo_progress = ((
						  self.genus_lookup_index * 1.0) / self.genus_hits_to_search) * 50
		cross_blast_progress = ((
								self.current_cross_query * 1.0) / self.queries_in_cross) * 50

		return phylo_progress + cross_blast_progress

	"""
	Sets the current ID for this job
	"""

	def set_id_number(self, id_number):
		self.id_number = id_number

	"""
	Returns the id_number of the localcrossblast
	"""

	def get_id_number(self):
		return self.id_number

	"""
	Returns the name of the query
	"""

	def get_query_name(self):
		return self.initial_query.get_query_name()

	"""
	Takes in a new request and runs the CrossBlast
	"""

	def remove_non_final_results(self):

		all_results = os.listdir(self.results_dir)

		for result in all_results:

			if not "FINAL" in result and ".csv" in result:
				remove_path = self.results_dir + result
				print "removing: " + result
				os.remove(remove_path)

	def delete_failed_data(self):

		shutil.rmtree(self.results_dir)

	def is_sequence_already_used(self, new_sequence):
		new_seq_name = self.get_file_from_path(new_sequence)
		used_seqs = []
		with open(self.saved_sequences, "r") as saved_seqs:
			data = saved_seqs.read()
			used_seqs = data.split('\n')

		for seq in used_seqs:
			if seq == new_seq_name:
				return True

		return False

	def save_used_sequence(self, sequence_location):
		file_name = self.get_file_from_path(sequence_location)
		with open(self.saved_sequences, "a") as save_file:
			save_file.write(file_name + "\n")

	def get_file_from_path(self, file_path):

		rev_path = file_path[::-1]
		file_name = ""
		for index, c in enumerate(rev_path):
			if c == "/":
				file_name = rev_path[:index][::-1]
				break

		return file_name

	def run_cross(self):
		if self.initial_query is not None:
			try:
				self.perform_initial_query()
				self.cross_blast_results()
				self.parse_relevant_genus_sequences()
				self.analyze_genus_data()
				self.remove_non_final_results()
			except ValueError as e:
				print "{0}".format(e)
				print "Seq was already blasted by this query"
				pass
			except Exception as e:
				print "{0}".format(e)
				print "Could not get genus data. Abandoning query and removing data ..."
				self.delete_failed_data()

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
