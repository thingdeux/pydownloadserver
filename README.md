#pyDownloadServer - Python web downloader
#Library Requirements: jinja2, cherrypy




#Current Dev Notes
**pyDownloader** (Web Daemon) - Run pyDownloader.py to start cherrypy server, port: 8000
	startWebServer() -Starts web server with checks for DB connection. Attempts to create local .database.db file if none exists.

**emailCrawl.py** (e-mail crawling helper)
    -queueAllEmailInbox() - function to use to kickoff crawling of e-mail inbox,pull download urls and queue them for download.  
    -listAllEmails() - function to return a list of all found urls in the inbox


**DownloadThread.py** (class definition for individual downloads)

**downloadManager.py** (handler for download events)
	-queueDownload(url, source = "web") - function to use when requesting a job queue for a url

**database.py**  functions for directly interacting with the DB
	