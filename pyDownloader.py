import cherrypy
import emailCrawl
import os
import downloader
import logger
import database
from mako.template import Template
from mako.lookup import TemplateLookup

VERSION = "0.3"
CURRENT_STATE = "debug"

# bind to all IPv4 interfaces and set port
current_folder = os.path.dirname(os.path.abspath(__file__))


cherrypy.config.update({ 'server.socket_host': '0.0.0.0',
                         'server.socket_port': 12334,
                         })

conf = {         
        '/static': { 'tools.staticdir.on' : True,
                      'tools.staticdir.dir': os.path.join(current_folder, 'static')
                    },
         '/static/css': { 'tools.staticdir.on' : True,
                          'tools.staticdir.dir': os.path.join(current_folder, 'static/css')
                        },
         '/js': { 'tools.staticdir.on' : True,
                      'tools.staticdir.dir': os.path.join(current_folder, 'js')
                    },
         '/js/lib': { 'tools.staticdir.on' : True,
                          'tools.staticdir.dir': os.path.join(current_folder, 'js/lib')
                        },
        'favicon.ico': {
                        'tools.staticfile.on': True,
                        'tools.staticfile.filename': os.path.join(current_folder, "/static/favicon.ico")
        },

        }




class webServer(object):            

    @cherrypy.expose
    def index(self, **arguments):       
        #Create the below template using index.html (and looking up in the static folder)
        mako_template = Template(filename='static/index.html')
        
        #Render the mako template and pass it the current_emails list variable
        self.mako_template_render = mako_template.render()                    

        return self.mako_template_render

    @cherrypy.expose
    def addUrlToQueue(self, **kwargs):
        try:            
            for url in kwargs:
                downloader.queueDownload(url)                            
        except:
            for url in kwargs:                
                logger.log("Unable to queue: " + url)

    @cherrypy.expose
    def history(self):
        #Create the below template using history.html (and looking up in the static folder)
        mako_template = Template(filename='static/history.html')

        historical_queue_results = database.getJobs("historical")           

        #Render the mako template and pass it the current_emails list variable
        mako_template_render = mako_template.render(historical_queue_data = historical_queue_results)

        return mako_template_render

    @cherrypy.expose
    def queue(self):       
        #Create the below template using queue.html (and looking up in the static folder)
        mako_template = Template(filename='static/queue.html')
        
        #DB query to get active jobs
        active_queue_results = database.getJobs("active")

        #Render the mako template and pass it the current_emails list variable
        mako_template_render = mako_template.render(active_queue_data = active_queue_results)

        return mako_template_render

    @cherrypy.expose
    def config(self):
        #Create the below template using config.html (and looking up in the static folder)
        mako_template = Template(filename='static/config.html')
        
        #DB query to get current parameters
        config_parameters = database.getConfig()

        #Render the mako template
        mako_template_render = mako_template.render(config_data = config_parameters)

        return mako_template_render   


def startWebServer():
    if database.verifyDatabaseExistence():

        try:
            if database.verifyDatabaseExistence():                    
                cherrypy.quickstart(webServer(), config=conf)
            
        except Exception, err:
            for error in err:
                logger.log("Unable to query DB - " + error)
    else:
        try:
            #Database doesn't exist, create it then recursively try again
            database.createFreshTables()
            if CURRENT_STATE is "debug":
                database.debugCreateTestData()
            startWebServer()
        except Exception, err:
            for error in err:
                logger.log("Unable to create DB: " + error)            
            
    
downloader.manageQueues()
startWebServer()