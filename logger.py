__author__ = 'josh'
import time

def log(error="Error", severity=4):	
	current_time = time.asctime(time.localtime(time.time()))
	the_error = str(current_time) + ": " + str(error)
	#This will change for debugging it's print	
	print(the_error)

def getTime():
	current_time = time.asctime(time.localtime(time.time()))
	return (current_time)