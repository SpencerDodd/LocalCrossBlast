from LocalCrossBlast import LocalCrossBlast
from FastaFileRequest import FastaFileRequest
import Tkinter, tkFileDialog

# GLOBAL VARIABLES
global database_location
database_location = "/Users/spencerdodd/Documents/Research/Khrapko_Lab/" \
					"Mitochondrial_Genomics/Scripts/ncbi-blast-2.3.0+/db/" \
					"pradodb.fsa"


def main():
	query_name = raw_input("What is the name of this query?\n")
	print "Please locate the query file"

	# - for file dialog -
	root = Tkinter.Tk()
	root.withdraw()
	query_file_path = tkFileDialog.askopenfilename()
	root.destroy()
	# -------------------

	# create the request
	new_request = FastaFileRequest(query_name, "blastn", database_location,
								   file_path=query_file_path)

	run_cross = LocalCrossBlast()
	run_cross.create_fasta_file_cross_blast(new_request)
	run_cross.perform_initial_query()
	run_cross.cross_blast_results()

if __name__ == "__main__":
	main()
