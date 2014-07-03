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
ACTIVE_DOWNLOADS = []

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
        
    while not isServerShuttingDown():
        #Check for stopped jobs and remove them
        purgeDownloads()

        if len(getDownloads()) < MAX_NUMBER_OF_DOWNLOADS:        
            #find all files in queued status
            files_in_active_status = database.getJobs("active")        
            
            for files in files_in_active_status:
                if files[2] == "Queued":
                    #Assigned DB table ID to UniqueID
                    uniqueID = files[0]
                    url = files[1]
                    defaultFileName = makeDownloadFileName(url)
                    downloadContainer = DownloadThread(url,TEMP_LOCATION, defaultFileName,uniqueID, download_semaphore)
                    #Set thread daemon flag, if server shuts down thread will terminate
                    downloadContainer.daemon = True                                
                    #start the downloaded thread
                    downloadContainer.start()                     
                    #Add to active downloads list
                    ACTIVE_DOWNLOADS.append(downloadContainer)
                
                #Don't create new threads if MAX_NUMBER_OF_DOWNLOADS has been reached.
                if len(getDownloads()) >= MAX_NUMBER_OF_DOWNLOADS:
                    break
                    

        #sleep for 1 seconds before trying to find new downloads
        time.sleep(1)

def getDownloads():
    return ACTIVE_DOWNLOADS

def purgeDownloads():    
    to_purge = []    
    for download_thread in ACTIVE_DOWNLOADS:
        if not download_thread.isAlive():
            #Queue the thread for deletion, if it's deleted immediately iteration /
            #May not complete properly.
            to_purge.append(download_thread)
    #Remove stopped downloads thread(s)
    for download_thread in to_purge:
        ACTIVE_DOWNLOADS.remove(download_thread)

