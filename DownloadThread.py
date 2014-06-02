__author__ = 'jason/josh'
import sh
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
        self.progress = None
        self.timeRemaining = None
        self.downloadSpeed = None
        self.downloadPercentage = None

    def __releaseAndExit(self):
        self.sema.release()
        exit()

    def updateStatus(self, line):
        value = codecs.encode(line, 'utf-8')
        splitup = string.rsplit(value, " ")

        if len(splitup) > 3:
            self.timeRemaining = string.strip(splitup[len(splitup) -1])
            self.downloadSpeed = string.strip(splitup[len(splitup) -2])
            self.downloadPercentage = string.strip(splitup[len(splitup) -3])
            if self.downloadPercentage == "": self.downloadPercentage = string.strip(splitup[len(splitup) -4])

    def run(self):
        #Aquire a lock based on number of allowed concurrent processes
        self.sema.acquire()

        #Check for Duplicate Files
        somenumber = 1
        while os.path.isfile(self.location_to_save):
            self.location_to_save = os.path.join(self.pathToSave, "(" + str(somenumber) + ")" + self.filename)            
            somenumber = somenumber + 1

        #Update the database to let everyone know we're now in downloading status
        database.updateJobStatus(int(self.threadID), "downloading")
        
        try: 
            p = sh.wget("-O",self.location_to_save, self.url, _err=self.updateStatus)
            p.wait()
        except Exception, err:
            for error in err:
                logger.log("Download Thread: " + str(self.threadID) + " - " + str(error))

        database.updateJobStatus(self.threadID, "successful")
        #following releases the lock so we can fire the next download
        self.__releaseAndExit()

def makeDownloadFileName(url):
    downloadFileName = url.split('/')[-1]
    return downloadFileName
    
