__author__ = "Spencer Dodd"

import time
import subprocess
from LocalBlastRequest import LocalBlastRequest

"""
Class to represent a query that is to be made to a BLAST server. This may be
either an online or local blast server. The query contains a BlastRequest
object containing the information to be passed to the server as a request. It
will additionally store the results of the query.
"""


class BlastQuery:

	def __init__(self, blast_request):

		self.query_start = "Started at ..."
		self.query_completed = "Ongoing ..."
		self.blast_request = blast_request
		self.blast_results = None


	"""
	Queries the blast server with the given query's request. The results of
	the query are stored in the Query object's blast_results field.
	"""
	def query_blast_server(self):

		"""
		If the request is a LocalBlastRequest, the command is carried out
		using a shell command call on the local system that accesses the
		local database.
		"""

		if isinstance(self.blast_request, LocalBlastRequest):

			command = self.blast_request.get_query_command()

			# update start time
			self.query_start = time.strftime('%X %x %Z')

			self.blast_results = subprocess.Popen(command, shell=True,
												  stdout=subprocess.PIPE).stdout

			# update completion time
			self.query_completed = time.strftime('%X %x %Z')

		else:

			raise Exception("Online BLASTing is not supported yet")