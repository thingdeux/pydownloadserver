import cherrypy
import emailCrawl

cherrypy.config.update({ 'server.socket_host': '127.0.0.1',
                         'server.socket_port': 12334,
                         })



class HelloWorld(object):


    @cherrypy.expose

    def index(self):
        #host = cherrypy.request.headers['Host']
        current_emails = emailCrawl.listAllEmails()
        builtPage = "<!DOCTYPE html> <html> <body> <h4> Inbox Downloads To Queue:</h4><ul>"

        for download_url in current_emails:
            builtPage = builtPage + "<li>" + str(download_url) + "</li>"

        builtPage = builtPage + "</ul></body></html>"

        return (builtPage)
    #index.exposed = True


cherrypy.quickstart(HelloWorld())