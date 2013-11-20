__author__ = 'jason'


#http://docs.python-requests.org/en/latest/index.html  -- The requests library
#do a pip install requests before running this

#Feature request: Each download should run on its own subprocess


import myDownload, time

def queueDownload(url):

    downloadFileName = url.split('/')[-1] #Gather the file name from the URL


#STATIC TEST DATA=======
test_url1 = "http://netstorage.unity3d.com/unity/UnitySetup-4.3.0.exe"
test_url2 = "http://www.google.com"
test_filename1 = test_url1.split('/')[-1]
test_filename2 = test_url2.split('/')[-1]
#=======================

#Creates 2 thread objects with the myDownload class.
thread1 = myDownload.myDownload(test_url1, test_filename1)
thread2 = myDownload.myDownload(test_url2, test_filename2)
#starts my test threads
thread1.start()
thread2.start()

#sleeps for a bit
time.sleep(10)

##tests the get process functions
print thread1.filename
thread1.getProgress()
print thread2.filename
thread2.getProgress()
