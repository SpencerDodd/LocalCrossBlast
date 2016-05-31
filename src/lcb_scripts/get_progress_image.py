#!/bin/python
import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import fnmatch
import os
from PIL import Image

save_path = "/Users/spencerdodd/Desktop/"
genus_results = []
genus_names = []
files = []

def analyze_genus_data():

	total_genuses = 0

	for root, dirnames, filenames in os.walk("/Volumes/Results/species"):
		for filename in fnmatch.filter(filenames, "FINAL_RESULTS.csv"):
			files.append(os.path.join(root, filename))
			total_genuses += 1

	for result_file in files:

		with open(result_file, "rb") as final_csv_file:

			reader = csv.reader(final_csv_file, delimiter = ',')

			for row in reader:

				genus_results.append(float(row[3]))
				if float(row[3]) > 3:
					print row[0] + " | " + row[3]

	"""# remove clearly wrong
	for index, result in enumerate(genus_results):

		if result > 10:
			print "removing result {0} | value: {1}".format(index, result)
			del genus_results[index]
	"""


	bin_max = max(genus_results)
	bins = np.linspace(0, bin_max, 10*bin_max)
	colors = ['dodgerblcolorue']
	plt.hist(genus_results, bins, alpha = 0.5, 
		label = '{0} (Range: {1} to {2} | Total Species: {3})'.format(
			'Species', min(genus_results), max(genus_results), total_genuses))

	plt.ylabel('Frequency')
	plt.xlabel('Percent dist to common ancestor')
	plt.title('Overview')
	plt.legend(loc = 'upper right')
	save_name = save_path + "Overview_species.png"
	os.remove(save_name)
	plt.savefig('{0}Overview_species.png'.format(save_path))

	photo = Image.open(save_name)
	photo.show()

analyze_genus_data()