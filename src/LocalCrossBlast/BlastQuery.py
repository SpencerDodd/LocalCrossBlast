__author__ = "Spencer Dodd"

import csv
import datetime
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
		self.blast_results_array = []

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
			dt = datetime.datetime.today()
			hour = dt.time().hour
			minute = dt.time().minute
			second = dt.time().second
			self.query_start = "{0}|{1}|{2}_{3}hour_{4}min_{5}sec".format(dt.year, dt.month, dt.day, hour, minute, second)

			print "performing: {0}".format(command)

			self.blast_results = subprocess.Popen(command, shell=True,
												  stdout=subprocess.PIPE).stdout

			# save the data from the request
			for result in self.blast_results:
				result_data = result.replace('|', "").split(',')
				self.blast_results_array.append(result_data)

			# update completion time
			dt2 = datetime.datetime.now()
			hour2 = dt2.time().hour
			minute2 = dt2.time().minute
			second2 = dt2.time().second
			self.query_completed = "{0}|{1}|{2}_{3}hour_{4}min_{5}sec".format(dt2.year, dt2.month,
														dt2.day, hour2, minute2, second2)

		else:

			raise Exception("Online BLASTing is not supported yet")

	"""
	Returns the database of the query's request
	"""

	def get_database(self):

		return self.blast_request.get_database()

	"""
	Saves the query results to a CSV file in the given directory
	"""

	def save_query_results(self, save_dir, query_type):

		save_name = ""

		if query_type == 'initial':
			save_name = "InitialResults_{0}_{1}.csv".format(
				self.blast_request.query_name, self.query_start)
		elif query_type == 'cross':
			save_name = "CrossResults_{0}_{1}.csv".format(
				self.blast_request.query_name, self.query_start)
		else:
			save_name = "UnknownQueryType_{0}_{1}.csv".format(
				self.blast_request.query_name, self.query_start)

		print "Writing BLAST results to file for {0} ...".format(
			self.blast_request.query_name)

		save_file = save_dir + save_name

		with open(save_file, 'wb') as f:

			c = csv.writer(f, delimiter=',')

			for index, line in enumerate(self.blast_results_array):

				print index, line

				if index == 0:
					c.writerow((['Query', 'Hit', 'Percent Similarity',
								 'Distance to Common Ancestor', 'Hit Seq',
								 'Hit Seq Len (bp)']))

				query = line[0]
				target = line[1]
				percent_sim = line[2].replace('\n', '')
				dist_to_common_anc = (100.0 - float(percent_sim)) / 2
				hit_seq = line[3]
				hit_len = len(hit_seq)

				c.writerow([query, target, percent_sim, dist_to_common_anc, hit_seq, hit_len])

		return save_dir + save_name

	"""
	Returns the name of the query
	"""
	def get_query_name(self):

		return self.blast_request.get_query_name()