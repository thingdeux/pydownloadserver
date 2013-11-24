import sqlite3
import os
import logger

current_path = os.path.dirname(os.path.abspath(__file__)	)
db_path = os.path.join(current_path, '.database.db')

def verifyDatabaseExistence():
#Check to see if DB exists
	if (os.path.isfile(db_path) ):
		try:
			db_connection = sqlite3.connect(db_path)
			db_connection.close()
			return(True)
		except Exception, err:			
			for i in err:
				logger.log("Unable to verify DB Existence - " + i)
	else:
		return(False)
	

def createFreshTables():
	#If DB doesn't exist create its tables and keys
	db_connection = sqlite3.connect(db_path)
	db = db_connection.cursor()
		
	db.execute('''CREATE TABLE jobs 
			(id INTEGER PRIMARY KEY, url TEXT, status TEXT, time_left INTEGER,
				time_queued INTEGER, source TEXT)''')
	db.execute('''CREATE TABLE config 
			(id INTEGER PRIMARY KEY, email_username TEXT, email_password TEXT, download_location INTEGER,
				pause_queue INTEGER)''')
	db.execute(''' CREATE INDEX sourceIndex ON jobs(source ASC) ''')
	db.execute(''' CREATE INDEX statusIndex ON jobs(status ASC) ''')

	db_connection.commit()
	db_connection.close()

def connectToDB():
	try:
		#If DB doesn't exist create its tables and keys
		db_connection = sqlite3.connect(db_path)
		db = db_connection.cursor()				
		return (db_connection)
	except Exception, err:
		for error in err:
			logger.log("Unable to connect to DB - " + error)
			return (False)

def debugCreateTestData():
	try:
		db_connection = connectToDB()
		db = db_connection.cursor()

		#Buid data string to insert
		jobsData = [
			(None, "http://i.imgur.com/NRfBaS6.jpg", "Queued", 0, logger.getTime(), source),
			(None, "http://i.imgur.com/NRfBaS6.jpg", "Queued", 0, logger.getTime(), source),
		]


	except: Exception, err:
		for error in err:
			logger.log(error)
			db.close()
def getJobs(resultRequested):
	try:
		db_connection = connectToDB()
		db = db_connection.cursor()

		if resultRequested is "all":
			db.execute('''SELECT * from jobs ''')
		elif resultRequested is "active":
			db.execute('''SELECT * from jobs WHERE status ="Queued" OR status = "Downloading" ''')
		elif resultRequested is "historical":
			db.execute('''SELECT * from jobs WHERE status = "Succesful" OR status = "Failed" ''')
		elif resultRequested is "failed":
			db.execute('''SELECT * from jobs WHERE status ="Failed" ''')
		elif resultRequested is "succesful":
			db.execute('''SELECT * from jobs WHERE status = "Succesful" ''')

		data = db.fetchall()		
		db_connection.close()

		return (data)
	except Exception, err:
		for error in err:
			logger.log("Unable to query DB - " + error)
		return(False)	

def insertJob(url, source):
	try:
		db_connection = connectToDB()
		db = db_connection.cursor()
		#Build job list to be inserted into DB
		job = [	(None, url, "Queued", 0, logger.getTime(), source)  ]
		#iterate over list and create insert command for DB
		db.executemany('INSERT INTO jobs VALUES (?,?,?,?,?,?)', job)			

		try:
			db_connection.commit()
			db_connection.close()
		except Exception, err:
			for error in err:
				logger.log(error)
				db.close()		
	except Exception, err:
		for error in err:
			db_connection.close()
			logger.log("Unable to insert record - " + error)






