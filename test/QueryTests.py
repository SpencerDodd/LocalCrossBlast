from LocalCrossBlast.FastaFileRequest import FastaFileRequest
from LocalCrossBlast.BlastQuery import BlastQuery
import unittest


class QueryTests(unittest.TestCase):

	# test that there is a result that is given from the local blasting of a
	# request of a query.
	def test_file_query(self):

		test_fasta_file_request = FastaFileRequest("seq_a", "blastn", "/Users/spencerdodd/Documents/Research/Khrapko_Lab/Mitochondrial_Genomics/Scripts/ncbi-blast-2.3.0+/db/pradodb.fsa", file_path="/Users/spencerdodd/Documents/Research/Khrapko_Lab/Mitochondrial_Genomics/Prado_Apes/individual_seqs/>Gorilla_beringei_graueri_A929_Kaisi")
		test_query = BlastQuery(test_fasta_file_request)

		self.assertTrue(test_query.blast_results is None)

		test_query.query_blast_server()

		self.assertTrue(test_query.blast_results is not None)