import os
from datetime import date, timedelta
import zipfile
import csv
try:
	from urllib.request import urlretrieve
except ImportError:
	from urllib import urlretrieve

class Parse():

	def __init__(self):
		self.fdate = (date.today()-timedelta(2)).strftime('%d%m%y')
		self.cwd = os.getcwd()
		self.zipname = self.fdate + ".zip"
		self.csvname = "EQ" + self.fdate + ".CSV"

	def obtain(self):

		urlretrieve("http://www.bseindia.com/download/BhavCopy/Equity/EQ" + self.fdate +  "_CSV.ZIP", self.zipname)

		zp = zipfile.ZipFile(self.cwd + "/" + self.zipname)
		zp.extractall()
		os.remove(self.zipname)
		zp.close()
		self.parse()
		os.remove(self.csvname)

	def parse(self):
		with open(self.csvname) as csvfile:
			eq = list(csv.DictReader(csvfile))