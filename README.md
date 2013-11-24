#pyDownloadServer - Python web downloader

#Current Dev Notes
**pyDownloader** (Web Daemon) - Run pyDownloader.py to start cherrypy server, port: 12334

**emailCrawl.py** (e-mail crawling helper)
    -queueAllEmailInbox() - function to use to kickoff crawling of e-mail inbox,
                                pull download urls and queue them for download.
    -listAllEmails() - function to return a list of all found urls in the inbox

**myDownload.py** (class definition)

**database.py - functions for interacting with the sqllite3 DB
	-verifyDatabaseExistence() - Used on server startup to make sure DB exists.
	-createFreshTables() - called by server to create a new,empty table with schema	
	-getJobs(requestedJob) -returns python list of jobs in the queue - can be passed the following params:
		--all
		--active
		--historical
		--failed
		--succesful
	-insertJob(url, source) -Insert a job into the download queue - (ex: of source can be web or email)
		--Source and status are indexed fields


Library Requirements: mako, cherrypy
	