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
        builtPage = "Inbox Downloads To Queue: \n\n"

        for download_url in current_emails:
            builtPage = builtPage + str(download_url) + "\n"

        return (builtPage)
    #index.exposed = True


cherrypy.quickstart(HelloWorld())