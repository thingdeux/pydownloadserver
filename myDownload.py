__author__ = 'jason'

#Feature request: Each download should run on its own subprocess

#test_url = "http://netstorage.unity3d.com/unity/UnitySetup-4.3.0.exe"
#test_url = "http://www.google.com"


import urllib2
import threading
import logger
import database
import os

class myDownload(threading.Thread):
    def __init__(self, url, pathToSave, filename, threadID, sema):
        threading.Thread.__init__(self)
        self.sema = sema
        self.threadID = threadID
        self.url = url
        self.filename = filename
        self.pathToSave = pathToSave
        self.location_to_save = pathToSave + filename
        self.progress = None
        self.response = None

    def __releaseAndExit(self):
        self.sema.release()
        exit()

    def __getResponsecode(self):
        code = self.response.code
        return code

    def getProgress(self):
        try:
            total_size = self.response.info().getheader('Content-Length').strip()
            total_size = int(total_size)
            bytes_so_far = 0
            chunk_size = 8192
            chunk = self.response.read(chunk_size)
            bytes_so_far += len(chunk)
            percent = float(bytes_so_far) / total_size
            percent = round(percent * 100, 2)
            return percent
        except:
            logger.log ("error retrieving progress")

    def run(self):
        #Aquire a lock based on number of allowed concurrent processes
        self.sema.acquire()

        #Try to open the file
        try:
            self.response = urllib2.urlopen(self.url)
        except:
            database.updateJobStatus(int(self.threadID), "failed") #Update status to failed
            logger.log("Error connecting to remote server to download file")
            self.__releaseAndExit()


        if self.__getResponsecode() == 200:
            #The following breaks down any downloading into memory manageable 32MB chunks.
            downloadable_chunk_size = 16*32768

            ##check if file name already exists, if so, add a number
            somenumber = 1
            while os.path.isfile(self.location_to_save):
                self.location_to_save = self.pathToSave + "(" + str(somenumber) + ")" + self.filename
                somenumber = somenumber + 1

            #open the file and save
            database.updateJobStatus(int(self.threadID), "downloading")
            with open(self.location_to_save, 'wb') as file_object:
                while True:
                    chunk = self.response.read(downloadable_chunk_size)
                    if not chunk: break
                    file_object.write(chunk)
            database.updateJobStatus(int(self.threadID), "successful") #Update status to failed
            #following releases the lock so we can fire the next download
            self.__releaseAndExit()

        else:
            logger.log("Server responded with a code other than 200")
            database.updateJobStatus(int(self.threadID), "failed") #Update status to failed
            #following releases the lock so we can fire the next download
            self.__releaseAndExit()