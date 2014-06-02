import cherrypy
import emailCrawl
import os
#import downloader
import logger
import database
import threading
from cherrypy.process.plugins import Monitor
from cherrypy.process.plugins import BackgroundTask
from jinja2 import Template, Environment, PackageLoader


VERSION = "0.3"
CURRENT_STATE = "debug"

# bind to all IPv4 interfaces and set port
current_folder = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=PackageLoader('main', 'templates'))

cherrypy.config.update({ 'server.socket_host': '0.0.0.0',
                         'server.socket_port': 8000,                        
                         })

conf = {         
        '/static': { 'tools.staticdir.on' : True,
                      'tools.staticdir.dir': os.path.join(current_folder, 'static')
                    },
         '/static/css': { 'tools.staticdir.on' : True,
                          'tools.staticdir.dir': os.path.join(current_folder, 'static/css')
                        },
         '/static/js': { 'tools.staticdir.on' : True,
                      'tools.staticdir.dir': os.path.join(current_folder, 'static/js')
                    },
         '/static/js/lib': { 'tools.staticdir.on' : True,
                          'tools.staticdir.dir': os.path.join(current_folder, 'static/js/lib')
                        },
        'favicon.ico': {
                        'tools.staticfile.on': True,
                        'tools.staticfile.filename': os.path.join(current_folder, "static/favicon.ico")
                        }
        }

class webServer(object):            

    @cherrypy.expose
    def index(self, **arguments):       
        #Create the below template using index.html        
        template = env.get_template('index.html')                                   
        return template.render()            
        

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
        #Create the below template using history.html
        template = env.get_template('history.html')
        historical_queue_results = database.getJobs("historical")                   
        return template.render(historical_queue_data = historical_queue_results)

    @cherrypy.expose
    def queue(self):       
        #Create the below template using queue.html
        template = env.get_template('queue.html')                
        #DB query to get active jobs
        active_queue_results = database.getJobs("active")
        #Render the jinja template and pass it the current_emails list variable
        return template.render(active_queue_data=active_queue_results)

    @cherrypy.expose
    def config(self):
        #Create the below template using config.html (and looking up in the static folder)        
        template = env.get_template('config.html')        
        #DB query to get current parameters
        config_parameters = database.getConfig()        
        
        return template.render(config_data=config_parameters)


def runCronJobs():
    if t1.isAlive():
        logger.log("Running")
    else:
        t1.start()
        logger.log("Started QueueManager")    

def startWebServer():
    if database.verifyDatabaseExistence():
        try:
            if database.verifyDatabaseExistence():
                #t1.start() #Start up the Backend Queue Manager
                #Register cherrypy monitor - runs every 30 seconds
                #EventScheduler = Monitor(cherrypy.engine, runCronJobs, 30, 'EventScheduler'  )
                #EventScheduler.start()
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

if __name__ == "__main__":
    #t1 = threading.Thread(target=downloader.manageQueues)
    startWebServer()    
        