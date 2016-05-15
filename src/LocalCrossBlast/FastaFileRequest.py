__author__ = "Spencer Dodd"

from LocalBlastRequest import LocalBlastRequest

"""
Class to represent a LocalBlastRequest that will be made with a Fasta-formatted
file.
"""


class FastaFileRequest(LocalBlastRequest):

	"""
	Constructor for a FastaFileRequest that contains a file path to the file
	that is to be the query sequence for the BLAST algorithm.
	"""
	def __init__(self, *args, **kwargs):

		LocalBlastRequest.__init__(self, *args)
		self.file_path = kwargs.get("file_path")

	"""
	Returns a string that is the query to be passed to the local BLAST server
	"""
	def get_query_command(self):

		query_command = "{0} -query '{1}' -db {2} -num_threads 2 -culling_limit 1 -num_alignments 50 -outfmt '10 qacc sacc pident sseq staxids'".format(self.algorithm_type, self.file_path, self.database)

		return query_command