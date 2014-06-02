__author__ = 'josh'
shutdownServer = False

def isServerShuttingDown():	
	global shutdownServer
	return shutdownServer

def setServerShuttingDown(status):
	global shutdownServer
	shutdownServer = status

def downloadStatus():
	#get active downloads
	return ("Active")