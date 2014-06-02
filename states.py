shutdownServer = False

def isServerShuttingDown():
	return shutdownServer

def setServerShuttingDown(status):
	shutdownServer = status

def downloadStatus():
	#get active downloads
	return ("Active")