from Tkinter import Tk, Text, TOP, BOTH, X, N, S, E, W, LEFT, RIGHT, BOTTOM, Listbox
from ttk import Frame, Label, Entry, Button
import tkFileDialog
from FastaFileRequest import FastaFileRequest
from LocalCrossBlast import LocalCrossBlast

"""
class FileQueryReturn():
	def __init__(self, query_name, file_location, database_location):
		self.query_name = query_name
		self.file_location = file_location
		self.database_location = database_location

	def get_query_name(self):
		return self.query_name

	def get_file_location(self):
		return self.file_location

	def get_database_location(self):
		return self.database_location

	def get_summary(self):

		print "{0}\n{1}\n{2}".format(self.get_query_name(),
									 self.get_file_location(),
									 self.get_database_location())
"""

global databases
databases = [
			["refseq_genomic", "refseq_genomic"],
			["prado_db", "/Users/spencerdodd/Documents/Research/Khrapko_Lab/Mitochondrial_Genomics/Scripts/ncbi-blast-2.3.0+/db/pradodb.fsa"],
			["full_mito_db", "/Users/spencerdodd/Documents/Research/Khrapko_Lab/Mitochondrial_Genomics/Scripts/ncbi-blast-2.3.0+/db/full_mito_db.fsa"]
			]

class GUIView(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		# variables

		self.parent = parent
		self.query_name = ""
		self.sequence_location = None
		self.database_location = None

		self.initUI()

	def initUI(self):

		self.parent.title("BLAST QUERY")
		self.pack(fill=BOTH, expand=True)

		# first frame, query name input

		frame1 = Frame(self)
		frame1.pack(fill=X)

		lbl1 = Label(frame1, text="Query Name", width=14)
		lbl1.pack(side=LEFT, padx=5, pady=5)

		entry1 = Entry(frame1)
		entry1.pack(fill=X, side=LEFT, anchor=W, padx=5, expand=True)
		# entry1.delete(0, "end")
		entry1.insert(0, str(self.query_name))
		set_entry1 = Button(frame1, text="Set",
							command=lambda: self.set_query_name(entry1.get()))
		set_entry1.pack(side=RIGHT, anchor=E, padx=5, pady=5)

		# second frame, sequence file location

		frame2 = Frame(self)
		frame2.pack(fill=X)

		lbl2 = Label(frame2, text="File Path", width=14)
		lbl2.pack(side=LEFT, padx=5, pady=5)

		entry2 = Entry(frame2)
		entry2.pack(fill=X, side=LEFT, anchor=W, padx=5, expand=True)
		entry2.delete(0, "end")
		entry2.insert(0, str(self.sequence_location))

		browser = Button(frame2, text="Find Seq", command=self.get_seq_loc)
		browser.pack(side=RIGHT, anchor=E, padx=5, pady=5)

		# third frame, database location

		frame3 = Frame(self)
		frame3.pack(fill=X)

		lbl3 = Label(frame3, text="Database", width=14)
		lbl3.pack(side=LEFT, anchor=N, padx=5, pady=5)

		listbox = Listbox(frame3, width=14, selectmode="single")
		listbox.pack(side=LEFT, padx=5, pady=5)

		for db in databases:
			listbox.insert("end", db[0])

		browser2 = Button(frame3, text="Set DB", command=lambda listbox=listbox: self.set_db(listbox.curselection()))
		browser2.pack(side=RIGHT, anchor=E, padx=5, pady=5)

		# fourth Frame, button frame

		frame4 = Frame(self)
		frame4.pack(fill=BOTH, expand=True)

		close_button = Button(frame4, text="Close", command=self.quit)
		close_button.pack(side=RIGHT, anchor=S, padx=5, pady=5)
		blast_button = Button(frame4, text="Run BLAST",
							  command=self.run_query)
		blast_button.pack(side=RIGHT, anchor=S, padx=5, pady=5)

	# gets the sequence location
	def get_seq_loc(self):
		self.sequence_location = tkFileDialog.askopenfilename()
		self.refresh_window()

	# gets the database location
	def set_db(self, db_selection):

		print db_selection

		self.database_location = databases[db_selection[0]][1]
		self.refresh_window()

	def refresh_window(self):
		self.destroy_all_widgets()
		self.initUI()

	def destroy_all_widgets(self):
		for widget in self.winfo_children():
			widget.destroy()

	def set_query_name(self, name):
		self.query_name = name
		self.refresh_window()

	def run_query(self):
		print "--------------- SELECTION DATA ---------------"
		print self.query_name
		print self.sequence_location
		print self.database_location
		print "----------------------------------------------"

		# create the request
		new_request = FastaFileRequest(self.query_name, "blastn",
									   self.database_location,
									   file_path=self.sequence_location)

		run_cross = LocalCrossBlast()
		run_cross.create_fasta_file_cross_blast(new_request)
		run_cross.perform_initial_query()
		run_cross.cross_blast_results()


def main():
	root = Tk()
	root.geometry("500x300+300+300")
	app = GUIView(root)
	root.mainloop()
