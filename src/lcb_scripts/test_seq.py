import Bio.SeqIO as SeqIO
import Bio.Entrez as Entrez

def run_it():
	accession = "Y10524.1"
	query_handle = Entrez.efetch(db="nucleotide", id=accession, rettype="gb", retmode="text")
	query_x = SeqIO.read(query_handle, 'genbank')
	query_name = query_x.annotations['organism']

	print query_name

run_it()