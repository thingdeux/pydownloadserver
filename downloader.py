__author__ = 'jason'


#import wget   Bail on this library, it's garbage - it will only print the status to the console.  Recommend Using requests instead
#It also only downloads locally to a tmp file - so the file will only ever save to where you run the script.  We'll roll our own implementation


#http://docs.python-requests.org/en/latest/index.html  -- The requests library
#do a pip install requests before running this

#Feature request: Each download should run on its own subprocess



import requests
import subprocess



def queueDownload(url):
    print("Downloading: " + url)
    #test_url = "http://netstorage.unity3d.com/unity/UnitySetup-4.3.0.exe"
    #downloaded_file = requests.get(url)



