import unittest

from LocalCrossBlast.LocalBlastRequest import LocalBlastRequest
from LocalCrossBlast.AccessionRequest import AccessionRequest
from LocalCrossBlast.FastaFileRequest import FastaFileRequest
from LocalCrossBlast.FastaStringRequest import FastaStringRequest


class BlastRequestTests(unittest.TestCase):

	global test_local_request, test_accession_request, test_fasta_file_request, test_fasta_string_request
	test_local_request = LocalBlastRequest("seq_a", "blastn", "/Users/spencerdodd/Documents/Research/Khrapko_Lab/Mitochondrial_Genomics/Scripts/ncbi-blast-2.3.0+/db/pradodb.fsa")
	test_accession_request = AccessionRequest("seq_a", "blastn", "/Users/spencerdodd/Documents/Research/Khrapko_Lab/Mitochondrial_Genomics/Scripts/ncbi-blast-2.3.0+/db/pradodb.fsa", accession_number="NC_086421")
	test_fasta_file_request = FastaFileRequest("seq_a", "blastn", "/Users/spencerdodd/Documents/Research/Khrapko_Lab/Mitochondrial_Genomics/Scripts/ncbi-blast-2.3.0+/db/pradodb.fsa", file_path="/Users/spencerdodd/Documents/Research/Khrapko_Lab/Mitochondrial_Genomics/Prado_Apes/individual_seqs/>Gorilla_beringei_graueri_A929_Kaisi")
	test_fasta_string_request = FastaStringRequest("seq_a", "blastn", "/Users/spencerdodd/Documents/Research/Khrapko_Lab/Mitochondrial_Genomics/Scripts/ncbi-blast-2.3.0+/db/pradodb.fsa", query_sequence=">seq_a\nACGTGGTCACACAACTGTCACTGCTAGCTAGCT")

	def test_query_command_creation(self):

		fasta_file_command = "blastn -query '/Users/spencerdodd/Documents/Research/Khrapko_Lab/Mitochondrial_Genomics/Prado_Apes/individual_seqs/>Gorilla_beringei_graueri_A929_Kaisi' -db /Users/spencerdodd/Documents/Research/Khrapko_Lab/Mitochondrial_Genomics/Scripts/ncbi-blast-2.3.0+/db/pradodb.fsa -outfmt '10 qacc sacc pident'"

		self.assertEqual(test_fasta_file_request.get_query_command(), fasta_file_command)