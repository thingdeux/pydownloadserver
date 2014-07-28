__author__ = 'jason/josh'
from requests import head, get
import os
import threading
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
        raise SystemExit

    def getProgress(self):
        return self.progress

    def download(self, url):
        def verifyValidUrl(header):
            try:
                if header.status_code == 200:
                    return True
                else:
                    return False
            except:
                return False

        def getFileSize(header):
            try:
                # HTTP Content-length header - converted to MB's
                file_size = int(header.headers['content-length']) / 1048576
                return float(file_size)
            except:
                return 0.0

        try:
            header = head(self.url)

            if verifyValidUrl(header):
                filesize = getFileSize(header)
                # http Get on the file location
                download = get(url, stream=True)
                # Update the current download
                downloaded = 0.0
                size = 1024000

                with open(self.location_to_save, 'wb') as f:
                    # Download and write in 1MB chunks - keeps memory usage
                    # down by downloading 1MB chunks
                    for data_chunk in download.iter_content(chunk_size=size):
                        if data_chunk:
                            f.write(data_chunk)
                            f.flush()
                            downloaded = downloaded + 1.0
                            # Get complete percentage
                            if filesize > 0.0:
                                if self.progress < 100:
                                    self.progress = (downloaded/filesize) * 100
                                elif self.progress >= 100:
                                    self.progress = 100
                            else:
                                self.progress = "--"
                return self.location_to_save
            else:
                logger.log("Invalid URL")
        except Exception, err:
            for error in err:
                logger.log("Invalid URL - " + str(error))

    def run(self):
        # Aquire a lock based on number of allowed concurrent processes
        self.sema.acquire()

        # Check for Duplicate Files
        somenumber = 1
        while os.path.isfile(self.location_to_save):
            self.location_to_save = os.path.join(self.pathToSave, "(" +
                                                 str(somenumber) + ")" +
                                                 self.filename)
            somenumber = somenumber + 1

        # Update status on DB
        database.updateJobStatus(int(self.threadID), "downloading")

        try:
            self.download(self.url)
        except Exception, err:
            for error in err:
                logger.log("Download Thread: " +
                           str(self.threadID) + " - " + str(error))

        database.updateJobStatus(self.threadID, "successful")
        # following releases the lock so we can fire the next download
        self.__releaseAndExit()
        return 0


def makeDownloadFileName(url):
    downloadFileName = url.split('/')[-1]
    return downloadFileName
