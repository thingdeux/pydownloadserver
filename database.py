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
			(id INTEGER PRIMARY KEY, config_type TEXT, name TEXT, value TEXT, html_tag TEXT, html_display_name)''')
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
	
	db_connection = connectToDB()
	db = db_connection.cursor()

	#Buid data string to insert
	jobsData = [
		(None, 'http://i.imgur.com/NRfBaS6.jpg', "Queued", 0, logger.getTime(), "email"),
		(None, 'http://c758482.r82.cf2.rackcdn.com/Sublime%20Text%202.0.2%20Setup.exe', "Queued", 0, logger.getTime(), "email"),
		(None, 'http://xxx.com/buttblasters11.avi', "Queued", 0, logger.getTime(), "email"),
		(None, 'http://xxx.com/buttblasters21.avi', "Failed", 0, logger.getTime(), "email"),
		(None, 'http://xxx.com/buttblasters1.avi', "Succesful", 0, logger.getTime(), "web"),
		(None, 'http://xxx.com/buttblasters2.avi', "Succesful", 0, logger.getTime(), "web"),
		(None, 'http://thisismeaddingaURL.com', "Downloading", 0, logger.getTime(), "email"),
		(None, 'http://i.imgur.com/lOOw9rq.gif', "Downloading", 0, logger.getTime(), "web"),
		(None, 'http://google.com/cockmunchers3.avi', "Queued", 0, logger.getTime(), "web"),
		(None, 'http://xxx.com/buttblasters16.avi', "Succesful", 0, logger.getTime(), "web"),
		(None, 'http://xxx.com/buttblasters16.avi', "Failed", 0, logger.getTime(), "email"),			
	]		

	configData = [
		(None,'E-Mail', 'email_username', 'pydownloadserver', 'text', 'GMail Username:'),
		(None,'E-Mail', 'email_password', 'Kaiser123', 'password', 'Gmail Password:'),
		(None,'General', 'download_path', current_path, 'text', "Download Location:"),
		(None,'Server', 'server_host', '0.0.0.0', 'text', "Host:"),
		(None,'Server', 'server_port', '12334', 'text', "Port")
		
	]

	db.executemany('INSERT INTO jobs VALUES (?,?,?,?,?,?)', jobsData)
	db.executemany('INSERT INTO config VALUES (?,?,?,?,?,?)', configData)

	try:
		db_connection.commit()
		db_connection.close()
		logger.log(logger.getTime() + " Inserted test data into db")
	except Exception, err:
		for error in err:
			logger.log("Unable to insert test data" + error)
			db_connection.close()
		
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
		elif resultRequested is "queued":
			db.execute('''SELECT * from jobs WHERE status = "Queued" ''')

		data = db.fetchall()		
		db_connection.close()

		return (data)
	except Exception, err:
		for error in err:
			logger.log("Unable to query DB - " + error)
			db_connection.close()
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
				db_connection.close()		
	except Exception, err:
		for error in err:
			db_connection.close()
			logger.log("Unable to insert record - " + error)

#Pull config info from the DB
def getConfig(config_name='all'):

	def tupleToList(passed_tuple):
		built_list = []
		for item in passed_tuple:
			built_list.append(item)

		return (built_list)

	if config_name == 'all' or config_name == '':
		try:
			db_connection = connectToDB()
			db = db_connection.cursor()		
			db.execute('''SELECT * from config''')
			config_data = db.fetchall()
			db_connection.close()

			return (config_data)

		except Exception, err:
				for error in err:
					logger.log("Unable to get config info - " + error)
					db_connection.close()
				return (False)	
	else:
		try:
			db_connection = connectToDB()
			db = db_connection.cursor()			
			db.execute('SELECT * FROM config WHERE name=?', (config_name,) )

			config_item = db.fetchall()			
			db_connection.close()

			return ( config_item )
		except Exception, err:
			for error in err:
				logger.log("Unable to get config info - " + error)
				db_connection.close()

def updateJobStatus(id,requestedStatus):
	
	try:
		db_connection = connectToDB()
		db = db_connection.cursor()

		if requestedStatus == "failed":
			db.execute('''UPDATE jobs SET status=? where id=?''', ("Failed", id,))
		elif requestedStatus == "downloading":
			db.execute('''UPDATE jobs SET status=? where id=?''', ("Downloading", id,))
		elif requestedStatus == "successful":
			db.execute('''UPDATE jobs SET status=? where id=?''', ("Successful", id,))
		elif requestedStatus == "queued":
			db.execute('''UPDATE jobs SET status=? where id=?''', ("Queued", id,))

		try:
			db_connection.commit()
			db_connection.close()
		except Exception, err:
			for error in err:
				logger.log(error)
				db_connection.close()
	except Exception, err:
		for error in err:
			db_connection.close()
			logger.log("Unable to update record - " + error)

#def deleteJobByID(id):

#def deleteJobByURL(url):
#def modifyConfiguration:

def changeJobStatusByID(job_id, new_status):

	if new_status in ('Succesful', 'Failed', 'Queued', 'Downloading'):

		try:
			db_connection = connectToDB()
			db = db_connection.cursor()		
			db.execute('UPDATE jobs SET status =:status WHERE id=:id', {"status":new_status, "id":job_id} )

			db_connection.commit()		
			db_connection.close()
			
		except Exception, err:
			for error in err:
				logger.log("Unable to modify job - " + error)
				db_connection.close()
	else:
		logger.log("Attempting to update job with an invalid status")

def modifyConfigurationItemByName(config_parameter_name, new_value):
	try:
		db_connection = connectToDB()
		db = db_connection.cursor()			
		db.execute('UPDATE config SET value = :new_value WHERE name = :name ', {"name": config_parameter_name, "new_value": new_value } )
		db_connection.commit()
		db_connection.close()
	
	except Exception, err:
		for error in err:
			logger.log("Unable to get config info - " + error)
			db_connection.close()