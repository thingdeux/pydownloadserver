__author__ = 'josh'
import cherrypy
import os
from downloadManager import queueDownload, queueManager, getDownloads
import logger
import database
import threading
from cherrypy.process.plugins import Monitor
from states import isServerShuttingDown
from states import setServerShuttingDown
from jinja2 import Environment, PackageLoader


VERSION = "0.3"
CURRENT_STATE = "debug"

# bind to all IPv4 interfaces and set port
current_folder = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=PackageLoader('main', 'templates'))
# Global manager singleton for handling thread var
manager = 0

cherrypy.config.update({'server.socket_host': '0.0.0.0',
                        'server.socket_port': 8000
                        })

conf = {
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(current_folder, 'static')
        },
    '/static/css': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(current_folder, 'static/css')
        },
    '/static/js': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(current_folder, 'static/js')
        },
    '/static/js/lib': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(current_folder, 'static/js/lib')
        },
    'favicon.ico': {
        'tools.staticfile.on': True,
        'tools.staticfile.filename': os.path.join(current_folder,
                                                  "static/favicon.ico")
        }
    }


class webServer(object):
    def __init__(self):
        cherrypy.engine.subscribe('stop', self.stop)

    @cherrypy.expose
    def index(self, **arguments):
        # Create the below template using index.html
        template = env.get_template('index.html')
        return template.render()

    @cherrypy.expose
    def addUrlToQueue(self, **kwargs):
        try:
            for url in kwargs:
                queueDownload(url)
        except:
            for url in kwargs:
                logger.log("Unable to queue: " + url)

    @cherrypy.expose
    def history(self, *args, **kwargs):
        try:
            if args[0] == "delete":
                database.deleteHistory("all")
        except:
            pass

        # Create the below template using history.html
        template = env.get_template('history.html')
        historical_queue_results = database.getJobs("historical")
        return template.render(historical_queue_data=historical_queue_results)

    @cherrypy.expose
    def queue(self):
        # Create the below template using queue.html
        template = env.get_template('queue.html')
        # DB query to get active jobs
        active_queue_results = database.getJobs("active")
        downloads = {}
        for active_thread in getDownloads():
            downloads[str(active_thread.threadID)] = str(active_thread.getProgress())  # noqa

        # ender the jinja template and pass it the current_emails list variable
        return template.render(active_queue_data=active_queue_results,
                               downloads=downloads)

    @cherrypy.expose
    def config(self):
        # Create the below template using config.html
        template = env.get_template('config.html')
        # DB query to get current parameters
        config_parameters = database.getConfig()

        return template.render(config_data=config_parameters)

    @cherrypy.expose
    def shutdown(self):
        template = env.get_template('shutdown.html')
        return template.render()

    @cherrypy.expose
    def stopServer(self):
        setServerShuttingDown(True)
        cherrypy.engine.exit()

    def stop(self):
        # Create the below template using config.html
        setServerShuttingDown(True)

    @cherrypy.expose
    def debug(self, *args):
        all_vars = globals()
        downloadies = getDownloads()
        template = env.get_template('debug.html')
        return template.render(debug_info=all_vars, downloads=downloadies)


def checkManager():
    # Register manager singleton as global
    global manager
    if not manager.isAlive() and not isServerShuttingDown():
        manager.start()


def startWebServer():
    global manager

    if database.verifyDatabaseExistence() and database.tableIntegrityCheck():
        try:
            manager = threading.Thread(target=queueManager)
            # Don't wait for thread to close on cherrypy exit stop method will
            # set the serverShuttingDown global to True
            # then the thread will exit
            manager.daemon = True
            manager.start()

            # Register cherrypy monitor - runs every 30 seconds
            EventScheduler = Monitor(cherrypy.engine, checkManager,
                                     30, 'EventScheduler')
            EventScheduler.start()

            cherrypy.quickstart(webServer(), config=conf)
        except Exception, err:
            for error in err:
                logger.log("Unable to start Web Server - " + str(error))
    else:
        try:
            # Database doesn't exist, create it then recursively try again
            database.createFreshTables()
            if CURRENT_STATE is "debug":
                database.debugCreateTestData()
            startWebServer()
        except Exception, err:
            for error in err:
                logger.log("Unable to create DB: " + error)
                logger.log("Your database may be corrupt, \
                            delete .database.db and try again")

if __name__ == "__main__":
    startWebServer()
