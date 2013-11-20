#pyDownloadServer - Python web daemon that accepts 
Library Requirements: mako, cherrypy

#Run pyDownloader.py to start cherrypy server, port: 12334



#Current Dev Notes
**pyDownloader** (Web Daemon) - run to start web server

**emailCrawl.py** (e-mail crawling helper)
    -queueAllEmailInbox() - function to use to kickoff crawling of e-mail inbox,
                                pull download urls and queue them for download.
    -listAllEmails() - function to return a list of all found urls in the inbox

**myDownload.py** (class definition)
	