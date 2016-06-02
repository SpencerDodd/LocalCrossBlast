# -*- coding: utf-8 -*-
from Tkinter import Tk, Text, TOP, BOTH, X, Y, N, S, E, W, LEFT, RIGHT, BOTTOM, \
	Listbox, IntVar, Scrollbar, VERTICAL, StringVar
from ttk import Frame, Label, Entry, Button, Progressbar
import tkFileDialog
from FastaFileRequest import FastaFileRequest
from LocalCrossBlast import LocalCrossBlast
import threading
import os

global databases
db_path = "/root/Research/ncbi-blast-2.4.0+/db/"
databases = [
	["prado_db",
	 "{}pradodb.fsa".format(db_path)],
	["full_mito_db",
	 "{}full_mito_db.fsa".format(db_path)],
	["subspecies_only",
	 "{}subspecies_only.fsa".format(db_path)]
]


# TODO
#	1. add a selection mode where a folder containing sequences can be
#		selected and all sequences inside the folder will be crossblasted
#	2. multithreading with deco to run more than 1 BLAST at once
#		- will likely need to be careful however, as program is very
#		resource intensive

class GUIView(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		# variables

		self.parent = parent
		self.query_name = ""
		self.sequence_location = None
		self.database_location = None
		# for handling
		self.new_crosses = []
		self.active_cross = IntVar(self)
		self.int_var = IntVar(self)
		self.folder_run = False
		self.folder_location = ""
		self.current_cross = StringVar(self)
		self.total_crosses = StringVar(self)
		self.percent_complete = StringVar(self)

		self.initUI()

	def initUI(self):

		self.set_current_cross(0)
		self.set_total_crosses(0)
		self.percent_complete.set(0)

		self.parent.title("CROSS BLAST")
		self.pack(fill=BOTH, expand=True)

		# first frame, sequence folder input
		frame0 = Frame(self)
		frame0.pack(fill=X)
		lbl0 = Label(frame0, text="Seq Folder BLAST", width=14)
		lbl0.pack(side=LEFT, padx=5, pady=5)
		entry0 = Entry(frame0)
		entry0.pack(fill=X, side=LEFT, anchor=W, padx=5, expand=True)
		entry0.delete(0, "end")
		entry0.insert(0, str(self.folder_location))
		browser = Button(frame0, text="Find Seq Folder", command=self.get_seq_folder_loc)
		browser.pack(side=RIGHT, anchor=E, padx=5, pady=5)


		# first frame, query name input
		frame1 = Frame(self)
		frame1.pack(fill=X)
		lbl1 = Label(frame1, text="Query Name", width=14)
		lbl1.pack(side=LEFT, padx=5, pady=5)
		entry1 = Entry(frame1)
		entry1.pack(fill=X, side=LEFT, anchor=W, padx=5, expand=True)
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
		browser2 = Button(frame3, text="Set DB",
						  command=lambda listbox=listbox: self.set_db(
							  listbox.curselection()))
		browser2.pack(side=RIGHT, anchor=E, padx=5, pady=5)

		# fourth Frame, progress bar
		frame4 = Frame(self)
		frame4.pack(fill=X)
		label0 = Label(frame4, text="Blast Queries", width=14)
		label0.pack(side=LEFT, anchor=N, padx=5, pady=5)
		self.listbox0 = Listbox(frame4, width=14, selectmode="single")
		self.listbox0.pack(side=LEFT, padx=5, pady=5)
		for cross_blast in self.new_crosses:
			new_cross_num = int(self.total_crosses.get())
			new_cross_num += 1
			self.total_crosses.set(new_cross_num)
			self.listbox0.insert("end", cross_blast.get_query_name())
		pb_hd = Progressbar(frame4, orient='horizontal', mode='determinate')
		pb_hd['variable'] = self.int_var
		pb_hd.pack(expand=True, fill=BOTH, side=TOP)
		total_progress_bar = Progressbar(frame4, orient='horizontal', mode='determinate')
		total_progress_bar['variable'] = self.percent_complete
		total_progress_bar.pack(expand=True, fill=BOTH, side=TOP)
		percent_complete_sign = Label(frame4, text="%", width=1)
		percent_complete_sign.pack(side=RIGHT, padx=5, pady=5)
		percent_complete_label = Label(frame4, textvariable=self.percent_complete, width=5)
		percent_complete_label.pack(side=RIGHT, padx=5, pady=5)
		progress_label_total = Label(frame4, textvariable=self.total_crosses, width=5)
		progress_label_total.pack(side=RIGHT, padx=5)
		progress_label_divider = Label(frame4, text="/", width=1)
		progress_label_divider.pack(side=RIGHT)
		progress_label_current = Label(frame4, textvariable=self.current_cross, width=5)
		progress_label_current.pack(side=RIGHT, padx=5, pady=5)


		# fifth Frame, add blast frame
		self.frame_blast = Frame(self)
		self.frame_blast.pack(fill=X)
		add_button = Button(self.frame_blast, text="Add BLAST",
							command=self.add_blast)
		add_button.pack(side=RIGHT, anchor=N, padx=5, pady=5)

		# fifth Frame, button frame
		frame5 = Frame(self)
		frame5.pack(fill=X)
		close_button = Button(frame5, text="Close", command=self.quit)
		close_button.pack(side=RIGHT, anchor=S, padx=5, pady=5)
		blast_button = Button(frame5, text="Run BLAST",
							  command=self.run_query_threaded)
		blast_button.pack(side=RIGHT, anchor=S, padx=5, pady=5)

		# sixth Frame, copyright frame
		self.frame6 = Frame(self)
		self.frame6.pack(fill=BOTH, expand=True)
		test_label = Label(self.frame6, text="© Spencer Dodd 2016")
		test_label.pack(side=RIGHT, anchor=N, padx=5, pady=5)

	# gets the location of a folder holding sequences
	def get_seq_folder_loc(self):
		self.folder_location = tkFileDialog.askdirectory(parent=self)
		self.refresh_window()
		self.folder_run = True

	# gets the sequence location
	def get_seq_loc(self):
		self.sequence_location = tkFileDialog.askopenfilename(parent=self)
		self.refresh_window()

	# gets the database location
	def set_db(self, db_selection):
		if len(db_selection) > 0:
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

	def set_active_cross(self, active_index):
		self.active_cross = active_index

	def add_blast(self):

		if not self.folder_run:

			if not self.is_file_data_empty(self.sequence_location):

				print "--------------- BLAST DATA ---------------"
				print self.query_name
				print self.sequence_location
				print self.database_location
				print "----------------------------------------------"

				# create the request
				new_request = FastaFileRequest(self.query_name, "blastn",
											   self.database_location,
											   file_path=self.sequence_location)

				new_cross_blast = LocalCrossBlast()
				new_cross_blast.create_fasta_file_cross_blast(new_request)
				new_cross_blast.set_id_number(len(self.new_crosses))
				self.new_crosses.append(new_cross_blast)

				self.refresh_window()
			else:
				print ("Seq file has no data: {0}".format(self.sequence_location))
		else:

			seq_files = self.filter_seq_files(os.listdir(self.folder_location))

			for sequence in seq_files:

				if ".FASTA" in sequence:

					seq_file_path = self.folder_location + "/" + sequence
					if not self.is_file_data_empty(seq_file_path):
						seq_name = sequence.replace(".FASTA", "").replace(" ", "_")

						seq_request = FastaFileRequest(seq_name, "blastn",
													   self.database_location,
													   file_path=seq_file_path)

						seq_cross_blast = LocalCrossBlast()
						seq_cross_blast.create_fasta_file_cross_blast(seq_request)
						seq_cross_blast.set_id_number(len(self.new_crosses))
						self.new_crosses.append(seq_cross_blast)
					else:

						print ("Seq file has no data: {0}".format(seq_file_path))

			self.refresh_window()



	def filter_seq_files(self, list_seq_dir):

		return list_seq_dir

	def run_query(self):
		for index, query in enumerate(self.new_crosses):
			self.set_current_cross(index + 1)
			self.set_percent_complete()
			query.run_cross()

	def set_percent_complete(self):
		percent_complete = float(float(self.current_cross.get()) / int(self.total_crosses.get()) * 100)
		shortened_percent = "{0:.2f}".format(percent_complete)
		self.percent_complete.set(shortened_percent)

	def set_current_cross(self, index):

		self.current_cross.set(int(index))

	def set_total_crosses(self, total):
		self.total_crosses.set(int(total))

	def run_query_threaded(self):
		# start the query
		self.secondary_thread = threading.Thread(target=self.run_query)
		self.secondary_thread.start()

		# start getting updates on progress
		self.tertiary_thread = threading.Thread(target=self.check_percentage)
		self.tertiary_thread.start()

	def set_active_cross_value(self):
		if len(self.listbox0.curselection()) < 1:
			self.active_cross.set(0)

		else:
			self.active_cross.set(self.listbox0.curselection()[0])

	def check_percentage(self):
		self.set_active_cross_value()

		if len(self.new_crosses) > 0:

			current_cross = self.new_crosses[self.active_cross.get()]
			self.int_var.set(current_cross.current_progress())
			# self.frame6.update()
			self.after(1, self.check_percentage)

		else:

			self.int_var.set(0)
			self.after(1, self.check_percentage())

	def is_file_data_empty(self, file_path):

		with open(file_path, "rb") as f:

			f_data = f.read().split("\n")
			if len(f_data) < 2:
				return True
			else:
				return False


def main():
	root = Tk()
	root.geometry("700x570+72500+0")
	root.attributes("-topmost", True)
	app = GUIView(root)
	root.mainloop()
