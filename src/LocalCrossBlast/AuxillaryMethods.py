"""
Methods for general use
"""
class AuxillaryMethods:

	def save_fasta_file(self, save_path, seq_name, fasta_string):

		with open(save_path, 'wb') as save_file:

			save_file.write(">" + seq_name + "\n")
			save_file.write(fasta_string)