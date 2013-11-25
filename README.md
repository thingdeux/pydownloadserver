#pyDownloadServer - Python web downloader
#Library Requirements: mako, cherrypy




#Current Dev Notes
**pyDownloader** (Web Daemon) - Run pyDownloader.py to start cherrypy server, port: 12334  

	startWebServer() -Starts web server with checks for DB connection. Attempts to create local .database.db file if none exists.

**emailCrawl.py** (e-mail crawling helper)

    -queueAllEmailInbox() - function to use to kickoff crawling of e-mail inbox,pull download urls and queue them for download.  
    -listAllEmails() - function to return a list of all found urls in the inbox  


**myDownload.py** (class definition)

**downloader.py** (handler for download events)
	-queueDownload(url, source = "web") - function to use when requesting a job queue for a url

**database.py**  functions for directly interacting with the sqllite3 DB

	-verifyDatabaseExistence() - Used on server startup to make sure DB exists.  
	-createFreshTables() - called by server to create a new,empty table with schema  
	-getConfig(parameter) - If called with no parameter, returns all config items, otherwise specify a string for name and a config item list will be returned.
			List Contents: id | config_type (ex: general, server, e-mail) | name (ex: email_password, server_host) | value | html_tag | html_display_name
			Example use: getConfig('email_username')  -or- getConfig()
	-getJobs(requestedJob) -returns python list of jobs in the queue - can be passed the following params:  

			1.	all  
			2.	active  (returns all queued/downloading)
			3.	historical  (returns all succesful/failed)
			4.	failed  (returns all failed)
			5.	succesful  (returns all succesful)

	-insertJob(url, source) -Insert a job into the download queue - (ex: of source can be web or email)  




	