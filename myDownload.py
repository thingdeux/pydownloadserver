__author__ = 'jason'

#Feature request: Each download should run on its own subprocess

#test_url = "http://netstorage.unity3d.com/unity/UnitySetup-4.3.0.exe"
#test_url = "http://www.google.com"


import urllib2
import threading
import logger


class myDownload(threading.Thread):
    def __init__(self, url, pathToSave, filename, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.url = url
        self.filename = filename
        self.location_to_save = pathToSave + filename #Change or make passable
        self.progress = None
        self.response = None

    def __getResponsecode(self):
        code = self.response.code
        return code

    def __saveToFile(self):
        #Some code here? Maybe pass the data over from run if you want to split them into two
        return False

    def run(self):
        #print self.filename + " is running"
        #self.response = urllib2.urlopen(self.url)  #You did a blind read here
        #if not self.__getResponsecode() == 200:
            #self.progress = self.__getResponsecode()
        #else:
            #print self.__getResponsecode()
            #self.__saveToFile()

        #The following breaks down any downloading into memory manageable 32MB chunks. 
        try:
            self.response = urllib2.urlopen(self.url)
        except:
            #need error handling to let us know wtf happened
            exit() #lets go ahead and kill this thread

        if self.__getResponsecode() == 200:

            downloadable_chunk_size = 16*32768

            #following locks the thread so no other threads can fire
            #threadLock.acquire()

            #open the file and save
            with open(self.location_to_save, 'wb') as file_object:
                while True:
                    chunk = self.response.read(downloadable_chunk_size)
                    if not downloadable_chunk_size: break
                    file_object.write(chunk)

        #following releases the lock so we can fire the next download
        #threadLock.release()


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

