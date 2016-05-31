import os
import shutil
save_path = "/Users/spencerdodd/Desktop/sub_seqs/"
seq_path = "/Users/spencerdodd/Desktop/all_individual_seqs/seqs/"
rejected_subspecies = [
	"mitochondrion",
	"mitochondrial",
	"x",
	"isolate",
	"strain",
	"voucher",
	"culture-collection",
	"sp.",
	"color",
	"1",
	"2",
	"3",
	"4",
	"5",
	"6",
	"7",
	"8",
	"9",
	"A",
	"B",
	"haplotype",
	"haplogroup",
	"clone",
	"var."
	]

accepted = []

def get_subspecies_seqs(seq_path):

	seqs = os.listdir(seq_path)

	for seq in seqs:

		seq_name = seq.split("__")
		if len(seq_name) > 1:

			name = seq_name[1].split("_")[2].replace(",","").replace("'","")
			
			if not name in rejected_subspecies:
				accepted.append(seq)

	for accept in accepted:
		print accept
	print len(accepted)

def save_accepted():

	for accept in accepted:

		new_path = seq_path+accept

		print "copying: {0} to {1}".format(new_path, save_path)
		shutil.copy(new_path, save_path)

get_subspecies_seqs(seq_path)
save_accepted()






