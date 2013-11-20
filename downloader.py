__author__ = 'jason'


#http://docs.python-requests.org/en/latest/index.html  -- The requests library
#do a pip install requests before running this

#Feature request: Each download should run on its own subprocess


import myDownload, threading

def queueDownload(url):

    downloadFileName = url.split('/')[-1] #Gather the file name from the URL



#STATIC TEST DATA=======
test_url1 = "http://netstorage.unity3d.com/unity/UnitySetup-4.3.0.exe"
test_url2 = "http://www.google.com"
test_filename1 = test_url1.split('/')[-1]
test_filename2 = test_url2.split('/')[-1]
#=======================

#Creates
thread1 = myDownload(test_url1, test_filename1)
thread2 = myDownload(test_url2, test_filename2)


for item in downloads:


thread1.start()
thread2.start()


time.sleep(10)

print thread1.filename
thread1.getProgress()
print thread2.filename
thread2.getProgress()

time.sleep(10)

