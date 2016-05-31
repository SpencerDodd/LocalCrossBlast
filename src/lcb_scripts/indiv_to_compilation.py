# Takes in a number of selected files and appends the content of the files into
# a single compilation file (for indiv seqs -> pre-mafft alignment)

import Tkinter, tkFileDialog
import datetime
import os

def indiv_to_compilation():

	# pulls all data from the selected files
	final_text = get_all_file_data()

	# date and time information for writing to file
	today = datetime.datetime.today().strftime('%y_%m_%d')
	hour = datetime.datetime.today().time().hour
	minute = datetime.datetime.today().time().minute
	second = datetime.datetime.today().time().second

	# output file to folder "Compilations", 1 level back from pwd
	file_path = '/Users/spencerdodd/Desktop/'

	# make dir if it doesn't already exist
	if not os.path.exists(file_path):

		os.makedirs(file_path)

	#file_name = file_path + 'seq_comp_' + today + '.txt'
	file_name = '%sseq_comp_%s_(%sh%sm%ss).txt' % (file_path, today, hour, minute, second)

	out_file = open(file_name, 'w')
	out_file.write(final_text)
	out_file.close()

# pulls all data from the selected files and returns the compiled data
def get_all_file_data():

	all_text = ''

	root = Tkinter.Tk()
	root.withdraw()
	file_paths = tkFileDialog.askopenfilenames()

	for path in root.tk.splitlist(file_paths):

		with open (path, 'r') as myfile:

			data = myfile.read().splitlines(True)

			for l in data:

				# make seq name 1 line (by replacing ' ' with '_')
				if l == data[0]:

					l = l.replace(' ', '_')

				all_text += l

			all_text += '\n'

	return all_text

# returns the pwd, minus one level of depth
def one_directory_back(current_directory):

	rev_dir = current_directory[::-1]

	rev_result = ''

	result = ''

	for c in rev_dir:

		if c == '/':

			rev_result += rev_dir[rev_dir.index(c):]
			
			result = rev_result[::-1]

			return result


def main():

	indiv_to_compilation()

main()










