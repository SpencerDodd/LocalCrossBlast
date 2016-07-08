"""
This is kind of a README.
This script works perfectly (maybe) if you are using a DB downloaded or compiled from the NCBI
with their naming formats. However, if you have compiled a database from your own set of
FASTA sequences (with makeblastdb) you will need to do a few things to ensure that everything
goes smoothly.
	1. in LocalCrossBlast.py, set the variable self.ncbi_parse_genus_info to False
		- This tells the program that the DB will not be querying the NCBI for phylogenetic
		information and should instead rely on the phylogenetic information supplied by the
		user and their sequence names.
	2. Ensure that sequence names used to compile the DB are formatted as follows:
		>{Genus}_{species}_{subspecies}_{accessionNumber}
		- This ensures that the phylogenetic parsing is completed correctly
"""