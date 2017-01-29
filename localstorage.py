import csv
import time

filename = 'localstorage.csv'

class LocalStorage:
	def getAll(self):
		file = open(filename, 'r+b')
		
		reader = csv.reader(file)
		entries = []
		for row in reader:
			entries.append(row)
		file.close()
		
		return entries
		
	def store(self, mode, token):
		file = open(filename, 'a')
		writer = csv.writer(file, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
		writer.writerow([mode, token, int(round(time.time() * 1000))])
		
	def clear(self):
		open(filename, 'w').close()
		