__author__ = 'jason'

#http://docs.python-requests.org/en/latest/index.html  -- The requests library
#do a pip install requests before running this

#Feature request: Each download should run on its own subprocess

#test_url = "http://netstorage.unity3d.com/unity/UnitySetup-4.3.0.exe"
#test_url = "http://www.google.com"

#downloaded_file = requests.get(test_url)

import urllib2, threading


class myDownload(threading.Thread):
    def __init__(self, url, filename):
        threading.Thread.__init__(self)
        self.url = url
        self.filename = filename
        self.progress = None
        self.response = None

    def __getResponsecode(self):
        code = self.response.code
        return code

    def __saveToFile(self):
        data = self.response.read()
        chunk_size = 2 * 1024
        with open(self.filename, "wb") as download:
            while True:
                print "we're successfully in write mode"
                chunk = data.read(chunk_size)
                if not chunk: break
                download.write(chunk)

    def run(self):
        print self.filename + " is running"
        self.response = urllib2.urlopen(self.url)
        if not self.__getResponsecode() == 200:
            self.progress = self.__getResponsecode()
        else:
            print self.__getResponsecode()
            self.__saveToFile()

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
            return "error retrieving progress"

