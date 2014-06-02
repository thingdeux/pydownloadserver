__author__ = 'jason/josh'
import time
import threading
import logger
import database
import os
from states import isServerShuttingDown
from DownloadThread import DownloadThread

#Global values
MAX_NUMBER_OF_DOWNLOADS = 2
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_LOCATION = os.path.join(CURRENT_DIR, 'tmp')

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

def cleanUpAfterCrash():    
    #Find all jobs in 'Downloading state'
    jobs_in_download_status = database.getJobs("downloading")

    #If a file is still in the queue as 'downloading' and hasn't been marked completed
    #But there is a file of the same name in the temp directory, set the jobs status to
    #Queued and remove the incomplete file
    for jobs in jobs_in_download_status:        
        url = jobs[1]        
        defaultFileName = makeDownloadFileName(url)
        save_location = os.path.join(TEMP_LOCATION, defaultFileName)
        if os.path.isfile(save_location): 
            os.remove(save_location)
    database.cleanUpAfterCrash()

def queueManager():
    cleanUpAfterCrash() #Do a clean up in case of crash    
    download_semaphore=threading.BoundedSemaphore(value=MAX_NUMBER_OF_DOWNLOADS)
    
    if not os.path.isdir(TEMP_LOCATION):
	    os.mkdir(TEMP_LOCATION)

    download_threads= []
    files_in_queued_status = []

    while not isServerShuttingDown():
        #find all files in queued status                
        files_in_active_status = database.getJobs("active")
        for files in files_in_active_status:
            if files[2] == "Queued":
                #Assigned DB table ID to UniqueID
                uniqueID = files[0]                
                url = files[1]
                defaultFileName = makeDownloadFileName(url)
                file_to_queue = [uniqueID, url]
                
                if not any(uniqueID in downloads for downloads in files_in_queued_status):
                    files_in_queued_status.append(file_to_queue) #Keeping track of what I've queued
                    downloadContainer = DownloadThread(url,TEMP_LOCATION, defaultFileName,uniqueID, download_semaphore)
                    downloadContainer.daemon = True
                    downloadContainer.start() #start the thread
                    download_threads.append(downloadContainer) #put it in a list to check on later        
        time.sleep(15) #sleep for 15 seconds before we try to find new downloads again