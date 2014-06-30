__author__ = 'jason/josh'
from requests import head, get, request
import os
import urllib2
import codecs
import time
import string
import threading
import datetime
import logger
import database

class DownloadThread(threading.Thread):
    def __init__(self, url, pathToSave, filename, threadID, sema):
        threading.Thread.__init__(self)
        self.sema = sema
        self.threadID = threadID
        self.url = url
        self.filename = filename
        self.pathToSave = pathToSave
        self.location_to_save = os.path.join(pathToSave, filename)
        self.progress = 0.0        

    def __releaseAndExit(self):
        self.sema.release()
        exit()

    def getProgress(self):
        return self.progress   

    def download(self,url):
        def verifyValidUrl(header):
            try:            
                if header.status == 200:
                    return True
                else:
                    return False
            except:
                return False

        def getFileSize(header):
            try:                            
                file_size = header.headers['content-length']
                return file_size
            except:
                return 0.0

        try:
            header = head(self.url)

            if verifyValidUrl(header):
                #Filesize (converted to MB's)
                filesize = float( int(getFileSize()) / 1048576 )        
                #http Get on the file location
                download = get(url, stream=True)
                #Update the current download 
                downloaded = 0.0

                with open(self.location_to_save, 'wb') as f:
                    #Download and write in 1MB chunks - keeps memory down downloading 1MB chunk at a time
                    for data_chunk in download.iter_content(chunk_size=1024000):
                        if data_chunk:
                            f.write(data_chunk)
                            f.flush()
                            downloaded = downloaded + 1.0
                            #Get complete percentage
                            self.progress = (downloaded/filesize) * 100                        
                return save_location 
            else:
                logger.log("Invalid URL")    
        except:
            logger.log("Invalid URL")
        

    def run(self):
        #Aquire a lock based on number of allowed concurrent processes
        self.sema.acquire()

        #Check for Duplicate Files
        somenumber = 1
        while os.path.isfile(self.location_to_save):
            self.location_to_save = os.path.join(self.pathToSave, "(" + str(somenumber) + ")" + self.filename)            
            somenumber = somenumber + 1

        #Update status on DB
        database.updateJobStatus(int(self.threadID), "downloading")
        
        try:                        
            self.download(self.url)
        except Exception, err:
            for error in err:
                logger.log("Download Thread: " + str(self.threadID) + " - " + str(error))

        database.updateJobStatus(self.threadID, "successful")
        #following releases the lock so we can fire the next download
        self.__releaseAndExit()

def makeDownloadFileName(url):
    downloadFileName = url.split('/')[-1]
    return downloadFileName
    
