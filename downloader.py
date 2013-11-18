__author__ = 'jason'


import wget
import subprocess
import os

test = "http://netstorage.unity3d.com/unity/UnitySetup-4.3.0.exe"

#def queueDownload(url):
#    filename = wget.download(url, bar=current)
#    return filename

filename = wget.download(test)
print filename