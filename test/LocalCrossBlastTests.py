from LocalCrossBlast import LocalCrossBlast
from LocalCrossBlast.FastaFileRequest import FastaFileRequest
import unittest
from mock import patch


class LocalCrossBlastTests(unittest.TestCase):

	def test_intialization(self):

		test_cross = LocalCrossBlast.LocalCrossBlast()

		self.assertEquals(test_cross.program_root_dir, "/Users/spencerdodd/"
													   "Documents/Research/"
													   "Khrapko_Lab/"
													   "LocalCrossBLAST/")
		self.assertEquals(test_cross.results_dir, "/Users/spencerdodd/"
												  "Documents/Research/"
												  "Khrapko_Lab/LocalCrossBLAST"
												  "/results/")


	# tests to ensure that a new query can be created with the provided mock
	# input for the name of the query and the location of the query file
	def test_query_creation(self):

		test_request = FastaFileRequest("seq_a", "blastn", "/Users/spencerdodd/Documents/Research/Khrapko_Lab/Mitochondrial_Genomics/Scripts/ncbi-blast-2.3.0+/db/pradodb.fsa", file_path="/Users/spencerdodd/Documents/Research/Khrapko_Lab/Mitochondrial_Genomics/Prado_Apes/individual_seqs/>Gorilla_beringei_graueri_A929_Kaisi")

		test_cross = LocalCrossBlast.LocalCrossBlast()

		with patch("__builtin__.raw_input", return_value="test") as _raw_input:

			with patch("tkFileDialog.askopenfilename", return_value="/Users/spencerdodd/Documents/Research/Khrapko_Lab/Mitochondrial_Genomics/Prado_Apes/individual_seqs/>Gorilla_beringei_graueri_9732_Mkubwa") as _raw_input:

				self.assertTrue(test_cross.initial_query is None)

				test_cross.create_fasta_file_cross_blast(test_request)
				test_cross.perform_initial_query()
				test_cross.cross_blast_results()

				self.assertTrue(test_cross.initial_query is not None)

	# tests for directory depth removal
	def test_directory_depth(self):

		root_dir = "/Users/spencerdodd/Documents/Research/Khrapko_Lab/LocalCrossBLAST/"
		one_dir = "/Users/spencerdodd/Documents/Research/Khrapko_Lab/LocalCrossBLAST/src"
		two_dir = "/Users/spencerdodd/Documents/Research/Khrapko_Lab/LocalCrossBLAST/src"

		test_cross = LocalCrossBlast.LocalCrossBlast()

		self.assertEquals(root_dir, test_cross.program_root_dir)