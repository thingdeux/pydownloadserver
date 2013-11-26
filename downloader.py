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

    print files_in_active_status

    #find all files in queued status
    for files in files_in_active_status:
        if files[2] == "Queued":
            uniqueID = files[0]
            url = files[1]
            defaultFileName = makeDownloadFileName(url)
            file_to_queue = [uniqueID, url]
            if not any(uniqueID in downloads for downloads in files_in_queued_status):
                print "I queued a download"
                files_in_queued_status.append(file_to_queue) #Keeping track of what I've queued
                downloadContainer = myDownload.myDownload(url,defaultPath, defaultFileName,uniqueID, download_semaphore)
                downloadContainer.start() #start the thread
                download_threads.append(downloadContainer) #put it in a list to check on later

#manageQueues()