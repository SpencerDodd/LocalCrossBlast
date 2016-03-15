__author__ = "Spencer Dodd"

"""
Class to represent a request that is to be made to a BLAST server. This could
be a request to either a local or online BLAST server. This is a base object
that is sub-classed for specificity in requests. The request will contain
a query and other necessary attributes for carrying out a BLAST search on a
database.
"""


class BlastRequest:

	def __init__(self):

		self.request = "BlastRequest"