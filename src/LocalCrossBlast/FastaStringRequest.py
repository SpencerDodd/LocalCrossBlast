__author__ = "Spencer Dodd"

from LocalBlastRequest import LocalBlastRequest

"""
Class to represent a LocalBlastRequest that will be made with a given FASTA-
formatted String
"""


class FastaStringRequest(LocalBlastRequest):

	"""
	Constructor for a FastaStringRequest that contains a String that is the
	FASTA sequence that is to be used in the BLAST query.
	"""
	def __init__(self, *args, **kwargs):

		LocalBlastRequest.__init__(self, *args)
		self.query_sequence = kwargs.get("query_sequence")

	"""
	Returns a string that is the query to be passed to the local BLAST server
	"""
	def get_query_command(self):

		raise Exception("Need to write seq string to file and use file.")

		query_command = "{0} -query {1} -db {2} -outfmt '10 qacc sacc pident'".format(self.algorithm_type, self.file_path, self.database)