# This is my README
Library Requirements: mako, cherrypy, requests

#Run pyDownloader to start cherrypy server, port: 12334

#emailCrawl.py
    queueAllEmailInbox() - function to use to kickoff crawling of e-mail inbox,
                                pull download urls and queue them for download.
    listAllEmails() - function to return a list of all found urls in the inbox
