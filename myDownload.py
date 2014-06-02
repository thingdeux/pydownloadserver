__author__ = 'jason'

#Feature request: Each download should run on its own subprocess

#test_url = "http://netstorage.unity3d.com/unity/UnitySetup-4.3.0.exe"
#test_url = "http://www.google.com"


import urllib2
import threading
import logger
import database
import os
import datetime


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
        self.chunk_variable_size = 1
        self.downloadable_chunk_size = self.chunk_variable_size*32768

    def __releaseAndExit(self):
        self.sema.release()
        exit()

    def __getResponsecode(self):
        code = self.response.code
        return code

    def __getAverageSpeed(self, list_of_speeds):
        ## speeds come in at a unit of bit per microsecond
        ## 
        number_of_items = 0
        sum_of_speeds = float(0)
        for speed in list_of_speeds:
            number_of_items = number_of_items + 1
            sum_of_speeds = sum_of_speeds + speed
            # print speed
        average_speed = sum_of_speeds/number_of_items
        # average_speed = (average_speed*1000000)/1024 #convert to kb
        #"{0:.2f}".format(
        return average_speed

    def getSpeed(self, chunk_size, date_time_start_of_chunk, date_time_end_of_chunk):
        delta_time = date_time_end_of_chunk - date_time_start_of_chunk
        bytes_over_time = chunk_size / float(delta_time.microseconds)
        return bytes_over_time

    def getTimeRemaining(self, bytes_so_far, speed):
        total_size = self.response.info().getheader('Content-Length').strip()
        amount_remaining = long(total_size)-long(bytes_so_far)
        # print str(amount_remaining)
        return (amount_remaining/speed)/100000

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
            
            ##check if file name already exists, if so, add a number
            somenumber = 1
            while os.path.isfile(self.location_to_save):
                self.location_to_save = self.pathToSave + "(" + str(somenumber) + ")" + self.filename
                somenumber = somenumber + 1

            ##Update the database to let everyone know we're now in downloading status
            database.updateJobStatus(int(self.threadID), "downloading")
            chunk_speeds = []
            chunk_loop_number = 0
            bytes_so_far = 0
            with open(self.location_to_save, 'wb') as file_object:
                while True:
                    #get_speed = False
                    
                    date_time_start_of_chunk = datetime.datetime.now()
                    chunk = self.response.read(self.downloadable_chunk_size)
                    if not chunk: break
                    date_time_end_of_chunk = datetime.datetime.now()
                    chunk_download_speed = self.getSpeed(len(chunk), date_time_start_of_chunk, date_time_end_of_chunk)

                    date_time_start_of_write = datetime.datetime.now()
                    file_object.write(chunk)
                    date_time_end_of_write = datetime.datetime.now()
                    chunk_write_speed = self.getSpeed(len(chunk), date_time_start_of_write, date_time_end_of_write)

                    bytes_so_far += len(chunk)

                    #try and find optimal chunking speed
                    if chunk_write_speed < chunk_download_speed:
                        self.chunk_variable_size = self.chunk_variable_size + .2

                    #Write time remaining & download speed once every 20 chunks to help reduce excessive database writes. 
                    if chunk_loop_number == 30:
                        reported_download_speed = self.__getAverageSpeed(chunk_speeds)
                        time_remaining = self.getTimeRemaining(bytes_so_far, reported_download_speed) #(reported_download_speed*1024)/1000000)
                        reported_time_remaining = "{0:.2f}".format(time_remaining) #time remaining in seconds

                        database_update_string = str(reported_time_remaining + " Sec @ " + "{0:.2f}".format((reported_download_speed/1024)*100000) + " KB/s")
                        database.updateTimeRemainingByID(self.threadID, database_update_string)
                        # print(str(reported_time_remaining) + " Sec @ " + str("{0:.2f}".format((reported_download_speed/1024)*100000) + " Kb/s"))
                        # print(str(self.response.info().getheader('Content-Length').strip()) + " total size")
                        # print(str(bytes_so_far) + " written")
                        chunk_loop_number = 0
                    chunk_loop_number = chunk_loop_number + 1
                    date_time_end_of_loop = datetime.datetime.now()
                    Total_Loop_Speed = self.getSpeed(len(chunk), date_time_start_of_chunk, date_time_end_of_loop)
                    chunk_speeds.append(Total_Loop_Speed)

            database.updateJobStatus(int(self.threadID), "successful")
            #following releases the lock so we can fire the next download
            self.__releaseAndExit()

        else:
            logger.log("Server responded with a code other than 200")
            database.updateJobStatus(int(self.threadID), "failed") #Update status to failed
            #following releases the lock so we can fire the next download
            self.__releaseAndExit()


###BELOW FOR TESTING###
def makeDownloadFileName(url):
    downloadFileName = url.split('/')[-1]
    return downloadFileName

if __name__ == '__main__':    
    max_number_of_downloads = 2
    download_semaphore=threading.BoundedSemaphore(value=max_number_of_downloads)
    
    test_url_1 = "http://ipv4.download.thinkbroadband.com/512MB.zip"
    test_url_2 = "http://ipv4.download.thinkbroadband.com/50MB.zip"
    test_file_name_1 = makeDownloadFileName(test_url_1)
    test_file_name_2 = makeDownloadFileName(test_url_2)

    t1 = myDownload(test_url_1, '/home/jason/tmp/', test_file_name_1, 1, download_semaphore)
    t2 = myDownload(test_url_2, '/home/jason/tmp/', test_file_name_2, 2, download_semaphore)

    # t1.start()
    t2.start()