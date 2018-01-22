import os
from datetime import date, timedelta, datetime
import zipfile
import csv
try:
	from urllib.request import urlretrieve
except ImportError:
	from urllib import urlretrieve
import redis

class Parse():

	def __init__(self):
		self.fdate = (date.today()).strftime('%d%m%y')							#keep track of today's date
		self.tnum = datetime.today().isoweekday()
		self.cwd = os.getcwd()
		self.zipname = self.fdate + ".zip"
		self.csvname = "EQ" + self.fdate + ".CSV"
		#self.red = redis.Redis('localhost')
		self.red = redis.from_url(os.environ.get("REDIS_URL"))

	def obtain(self):

		'''
			IMPORTANT: Do not un-comment the following two lines on the first use

			The following code, sort of automates the process of updating redis database.

			It will update during the first session of every working day, Tuesday through Saturday.

			Only un-comment after deploying the webapp and running the first session.
		'''

		#if (self.fdate == (self.red.lrange("last_updated", 0, 0)[0]).decode('UTF-8')):    	#checks if the database already exists
		#	return (self.fromdb())															#return db if it does

		#else 
		urlretrieve("http://www.bseindia.com/download/BhavCopy/Equity/EQ" + self.fdate +  "_CSV.ZIP", self.zipname) #retrieve zip file

		zp = zipfile.ZipFile(self.cwd + "/" + self.zipname)
		zp.extractall()
		os.remove(self.zipname)
		zp.close()
		req = self.parse()
		os.remove(self.csvname)													#extract, parse and finally remove unnecessary files
		return (req)

	def parse(self):
		self.red.flushall()														#flushing yesterday's database

		with open(self.csvname) as csvfile:
			eq = list(csv.DictReader(csvfile))									#parsing csv

		for name in eq:
			value = {'Name' : name['SC_NAME'].rstrip(), 'Code' : name['SC_CODE'], 'Open' : name['OPEN'], 'Close' : name['CLOSE'], 'High' : name['HIGH'], 'Low' : name['LOW']}
			self.red.hmset(name['SC_NAME'].rstrip(), value)						#set dict to an hash in redis
			self.red.rpush("insertion_order", name['SC_NAME'].rstrip())			#keep track of names in a different list

		self.red.lpush("last_updated", self.fdate)								#keep track of last update date
		return (self.fromdb())

	def fromdb(self):
		top_10_entires = self.red.lrange("insertion_order", 0, 9)				#get the first 10 entries in the redis database
		req = []																#to fetch and add them to an array
		for entry in top_10_entires:
			reg = self.red.hgetall(entry)
			req.append(reg)
		return req

	def last_update(self):
		return ((self.red.lrange("last_updated", 0, 0)[0]).decode('UTF-8'))		#return the last update date

	def search(self, q):														#searching for a particular entry and returing the same if it exists
			return (self.red.hgetall(q))