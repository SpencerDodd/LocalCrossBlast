__author__ = "Spencer Dodd"

from LocalBlastRequest import LocalBlastRequest
from AuxillaryMethods import AuxillaryMethods

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
		self.save_path = kwargs.get("save_path") + self.query_name + ".txt"
		self.query_sequence = kwargs.get("query_sequence")

	"""
	Returns a string that is the query to be passed to the local BLAST server
	"""
	def get_query_command(self):

		AuxillaryMethods().save_fasta_file(self.save_path, self.query_name, self.query_sequence)

		query_command = "{0} -query {1} -db {2} -outfmt '10 qacc sacc pident sseq'".format(self.algorithm_type, self.save_path, self.database)

		return query_command