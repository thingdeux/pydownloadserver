__author__ = 'jason'


#http://docs.python-requests.org/en/latest/index.html  -- The requests library
#do a pip install requests before running this

#Feature request: Each download should run on its own subprocess

import myDownload
import time
import threading
import logger
import database

def queueDownload(url, source="web"):
	try:
		#Gather the file name from the URL		
		logger.log("downloader Received Queue req: " + url + " | " + source)
		downloadFileName = url.split('/')[-1]
		database.insertJob(url, source)
	except Exception, err:
		for error in err:
			logger.log("Unable to queue url - " + error)


def testFunction():

	#STATIC TEST DATA=======
	test_url1 = "http://netstorage.unity3d.com/unity/UnitySetup-4.3.0.exe"
	test_url2 = "http://www.google.com"
	test_filename1 = test_url1.split('/')[-1]
	test_filename2 = test_url2.split('/')[-1]
	#=======================

	#Creates 2 thread objects with the myDownload class.
	thread1 = myDownload.myDownload(test_url1, test_filename1)
	#thread2 = myDownload.myDownload(test_url2, test_filename2)
	#starts my test threads
	thread1.start()
	#thread2.start()	

	##tests the get process functions
	#print thread1.filename
	#thread1.getProgress()
	#print thread2.filename
	#thread2.getProgress()



class aTestThread(threading.Thread):
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self) #Overriding default init
		self.threadID = threadID
		self.name = name
		self.counter = counter		

	def run(self):
		for i in range(100):
			print (str(i)),
		print("")
def testThreading():
	thread1 = aThread(1, "Uno", 1)
	thread2 = aThread(2, "Uno", 2)

	thread1.start()
	thread2.start()



#testFunction()
#testThreading()