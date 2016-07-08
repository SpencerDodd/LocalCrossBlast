import subprocess
import os

save_dir = '/Users/spencerdodd/Documents/Research/Khrapko_Lab/Mitochondrial_Genomics/Prado_Apes/individual_seqs/'
seq_file = '/Users/spencerdodd/Downloads/pradodb.fsa'


# reads the data from the seq file
def read_file(sequence_file):

	with open(sequence_file, 'r') as seq:

		data = seq.read()

		split_seqs(data)

		seq.close()

# splits the given string into individual sequences
def split_seqs(data_string):

	# read the string and split it by '>' character
	indiv_seqs = data_string.split('>')

	for seq in indiv_seqs:

		seq = '>' + seq

		save_file(seq)


# saves the given string as a seq file
def save_file(seq):

	file_name = seq.splitlines()[0].replace("/", "_")

	save_name = save_dir + file_name

	with open(save_name, 'wb') as save_file:

		save_file.write(seq)

		save_file.close()


# starts the show
def main():

	read_file(seq_file)

if __name__ == '__main__':

	main()








