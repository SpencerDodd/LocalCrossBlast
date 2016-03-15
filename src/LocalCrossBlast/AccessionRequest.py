__author__ = "Spencer Dodd"

from LocalBlastRequest import LocalBlastRequest

"""
Class to represent a LocalBlastRequest that will be made with an NCBI accession
number.
"""


class AccessionRequest(LocalBlastRequest):

	"""
	Constructor for a AccessionRequest that contains a string representing an
	NCBI sequence accession number
	"""
	def __init__(self, *args, **kwargs):

		LocalBlastRequest.__init__(self, *args)
		self.accession_number = kwargs.get("accession_number")

	"""
	Returns a string that is the query to be passed to the local BLAST server
	"""
	def get_query_command(self):

		raise Exception("Need to get seq file from accession #.")

		query_command = "{0} -query {1} -db {2} -outfmt '10 qacc sacc pident'".format(self.algorithm_type, self.file_path, self.database)