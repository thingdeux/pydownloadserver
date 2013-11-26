__author__ = 'jason'


#http://docs.python-requests.org/en/latest/index.html  -- The requests library
#do a pip install requests before running this

#Feature request: Each download should run on its own subprocess

import myDownload
import time
import threading
import logger
import database
import os

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


def makeDownloadFileName(url):
    downloadFileName = url.split('/')[-1]
    return downloadFileName


def manageQueues():


    max_number_of_downloads = 2


    download_semaphore=threading.BoundedSemaphore(value=max_number_of_downloads)


    #threadLock = threading.Lock()

    ThreadStatusDebug = True

    defaultPath = os.path.dirname(os.path.abspath(__file__))
    defaultPath = defaultPath + '/tmp/'
    if not os.path.isdir(defaultPath):
	    os.mkdir(defaultPath)


    download_threads= []
    files_in_active_status = database.getJobs("active")
    files_in_queued_status = []


    #find all files in queued status
    for files in files_in_active_status:
        if files[2] == "Queued":
            uniqueID = files[0]
            url = files[1]
            defaultFileName = makeDownloadFileName(url)
            file_to_queue = [uniqueID, url]
            if not any(uniqueID in downloads for downloads in files_in_queued_status):
                files_in_queued_status.append(file_to_queue) #Keeping track of what I've queued
                downloadContainer = myDownload.myDownload(url,defaultPath, defaultFileName,uniqueID, download_semaphore)
                #downloadContainer.start() #start the thread
                download_threads.append(downloadContainer) #put it in a list to check on later



    #not sure if this is actually working thanks to how fast its downloading.
    #I'll need a beefy file to download to test this portion.
    if ThreadStatusDebug == True:
        for t in download_threads:
            t.start()





            #print "sent start command"
            #if t.isAlive == True:
            #    print str(t.threadID) + "is alive"
            #else:
            #    print str(t.threadID) + "Terminated"




#manageQueues()

#testFunction()
#testThreading()