__author__ = "Spencer Dodd"

from FastaFileRequest import FastaFileRequest
from FastaStringRequest import FastaStringRequest
from BlastQuery import BlastQuery
import os
import datetime

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
		for result in self.initial_query.blast_results_array:

			query_name = result[0]
			hit_name = result[1]
			hit_seq = result[3]
			genus_prompt = "Is {0} related to {1} by genus level? (please enter 'y' or 'n': ".format(
				query_name, hit_name)

			is_genus_level = raw_input(genus_prompt)

			print is_genus_level

			if is_genus_level == "y":
				self.initial_results_to_cross.append([hit_name, hit_seq])
			else:
				break


	"""
	Creates queries for each of the initial blast query results. This is the
	cross-blasting section of the blast.
	"""


	def cross_blast_results(self):
		print "CrossBLAST'ing results"

		self.add_initial_genus_phylogenetic_info()

		for query in self.initial_results_to_cross:

			query_name = query[0]
			query_seq = query[1]

			current_query_request = FastaStringRequest(query_name, "blastn", self.query_database,
							   query_sequence=query_seq, save_path=self.temp_save_path)

			current_query = BlastQuery(current_query_request)
			self.cross_queries.append(current_query)

		for cross_query in self.cross_queries:

			print "BLAST'ing {0}".format(cross_query.blast_request.query_name)

			cross_query.query_blast_server()
			cross_query.save_query_results(self.results_dir, 'cross')


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
