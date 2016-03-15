__author__ = "Spencer Dodd"

from FastaFileRequest import FastaFileRequest
from BlastQuery import BlastQuery
import os
import time

"""
Represents the main control class for performing a local Cross Blast. Contains
the location of the local database, the file system heirarchy for file reading
and output, and is the source-point for creating and performing queries with
requests.
"""


class LocalCrossBlast:

	def __init__(self):

		self.program_root_dir = self.one_directory_back(os.getcwd())
		self.results_dir = self.program_root_dir + "results/"
		self.query_database = None
		self.initial_query = None
		self.cross_queries = []

		# make dirs that have not been created that the program requires
		self.make_dir(self.results_dir)

	# ------------------------------- METHODS ---------------------------------
	"""
	Creates a new fasta file request and query object and stores it in this
	object's 'queries' field
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
	Queries the blast server for the initial query results
	"""
	def perform_initial_query(self):

		pass

	"""
	Creates queries for each of the initial blast query results. This is the
	cross-blasting section of the blast.
	"""
	def cross_blast_results(self):

		pass

	# --------------------------- HELPER METHODS ------------------------------

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

