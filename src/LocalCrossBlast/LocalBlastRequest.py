__author__ = "Spencer Dodd"

import json
from BlastRequest import BlastRequest

"""
Class to represent a request that will be made to a local BLAST server. This
request will contain a query sequence name. It is sub-classed by various
sub-classes that will define whether the request will be made via FASTA
sequence string, FASTA sequence file, or accession number.
"""


class LocalBlastRequest(BlastRequest):

	"""
	Constructor for a BLAST request that takes in a query sequence name
	"""
	def __init__(self, query_name, algorithm_type, database):

		self.request_type = "LocalBlastRequest"
		self.query_name = query_name
		self.algorithm_type = algorithm_type
		self.database = database

	"""
	Returns a json-ified version of this object
	"""
	def jsonify(self):

		return json.dumps(self.__dict__)

	"""
	Returns a query command for the blast search
	"""
	def get_query_command(self):

		raise Exception("Base class has no query command")

	"""
	Returns the database of the request
	"""
	def get_database(self):

		return self.database

	"""
	Returns the name of the query
	"""
	def get_query_name(self):

		return self.query_name