#pyDownloadServer - Python web downloader

#Current Dev Notes
**pyDownloader** (Web Daemon) - Run pyDownloader.py to start cherrypy server, port: 12334

**emailCrawl.py** (e-mail crawling helper)
    -queueAllEmailInbox() - function to use to kickoff crawling of e-mail inbox,
                                pull download urls and queue them for download.
    -listAllEmails() - function to return a list of all found urls in the inbox

**myDownload.py** (class definition)

Library Requirements: mako, cherrypy
	