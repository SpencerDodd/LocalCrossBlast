#!/bin/python
import matplotlib.pyplot as plt
import numpy as np
import csv
import sys

file_path = "/Users/spencerdodd/Desktop/test"

genus_results = []

def analyze_genus_data():

	final_csv_path = file_path + "/FINAL_RESULTS.csv"

	with open(final_csv_path, "rb") as final_csv_file:

		reader = csv.reader(final_csv_file, delimiter = ',')

		for row in reader:

			print row
			genus_results.append(float(row[3]))

	bin_max = 10
	bins = np.linspace(0, bin_max, 200)
	colors = ['dodgerblcolorue']
	plt.hist(genus_results, bins, alpha = 0.5, label = '{0} (Range: {1} to {2})'.format('Genus', min(genus_results), max(genus_results)))

	plt.ylabel('Frequency')
	plt.xlabel('Percent dist to common ancestor')
	plt.title('Overview')
	plt.legend(loc = 'upper right')
	plt.savefig('{0}/Overview.png'.format(file_path))

analyze_genus_data()