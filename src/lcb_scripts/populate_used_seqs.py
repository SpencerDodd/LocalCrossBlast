import os

sequence_location = "/Users/spencerdodd/Desktop/all_individual_seqs/seqs/gi_49619212_ref_NC_005963.1__Amblyomma_triguttatum_mitochondrion,_complete_genome.FASTA"
new_sequence_location = "/Users/spencerdodd/Desktop/all_individual_seqs/seqs/gi_49619212_ref_NC_005963.1__Amblyomma_triguttatum_mitochondrion,_complete_genome.FASTA"
saved_sequences = "/Users/spencerdodd/Desktop/saved_seqs/used.txt"

def is_sequence_already_used(new_sequence):
	new_seq_name = get_file_from_path(new_sequence)
	used_seqs = []
	with open(saved_sequences, "r") as saved_seqs:
		data = saved_seqs.read()
		used_seqs = data.split('\n')

	for seq in used_seqs:
		if seq == new_seq_name:
			print "USED"
			return True

	print "NOT USED"
	return False


def save_used_sequence(sequence_location):
	file_name = get_file_from_path(sequence_location)
	with open(saved_sequences, "a") as save_file:
		save_file.write(file_name + "\n")

def get_file_from_path(file_path):

	rev_path = file_path[::-1]
	file_name = ""
	for index,c in enumerate(rev_path):
		if c == "/":
			file_name = rev_path[:index][::-1]
			break

	return file_name

save_used_sequence(sequence_location)
is_sequence_already_used(new_sequence_location)