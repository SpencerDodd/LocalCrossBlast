import os
import sys

"""
The function of this script is to rename the files and names of FASTA sequences to remove
problematic punctuation (commas) from the file. Presence of this punctuation has been disruptive
to the CSV output format that is utilized by the CrossBlast algorithm.
"""

sequence_directory = "/root/Research/mito_phylo/LocalCrossBlast/seqs/sub_seqs/"


def reformat_seq_files():
	print "Reformatting seq files ..."
	for seq_file in os.listdir(sequence_directory):
		print "Current file: {}".format(seq_file)

		if "," in seq_file:
			print "Dirty punctuation found. Reformatting beginning ..."
			dirty_file_path = sequence_directory + seq_file
			f = open(dirty_file_path, 'r')
			lines = f.readlines()
			lines[0] = clean_string(lines[0])

			clean_file_path = clean_string(dirty_file_path)
			clean_f = open(clean_file_path, 'w')
			clean_f.writelines(lines)
			f.close()
			clean_f.close()

			print "{} successfully reformatted".format(clean_string(seq_file))
			print "Deleting old file ..."

			delete_dirty_file(dirty_file_path)
		else:
			print "File is clean. Passing ..."


def delete_dirty_file(dirty_file_path):
	try:
		os.remove(dirty_file_path)
	except:
		print "File path given to remove does not exist: {}".format(dirty_file_path)


def clean_string(dirty_string):
	return dirty_string.replace(",","")


def main():
	reformat_seq_files()

if __name__ == "__main__":
	main()











