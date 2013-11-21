import cherrypy
import emailCrawl
import os
from mako.template import Template
from mako.lookup import TemplateLookup
#current_folder = os.path.dirname(__file__)

# bind to all IPv4 interfaces and set port

current_folder = os.path.dirname(__file__)


cherrypy.config.update({ 'server.socket_host': '0.0.0.0',
                         'server.socket_port': 12334,
                         })

conf = { '/static': { 'tools.staticdir.on' : True,
                      'tools.staticdir.dir': os.path.join(current_folder, 'static')
                    },
         '/static/css': { 'tools.staticdir.on' : True,
                          'tools.staticdir.dir': os.path.join(current_folder, 'static/css')
                        }                  
        }




class webServer(object):            

    @cherrypy.expose
    def index(self):       
        #Create the below template using index.html (and looking up in the static folder)
        mako_template = Template(filename='static/index.html')
        
        #Render the mako template and pass it the current_emails list variable
        mako_template_render = mako_template.render()

        return mako_template_render


    @cherrypy.expose
    def history(self):
        #Create the below template using history.html (and looking up in the static folder)
        mako_template = Template(filename='static/history.html')

        #Run the python command listAllEmails (from emailCrawl.py) to receive a python list of urls from the inbox.
        #current_emails = emailCrawl.listAllEmails()  

        #Putting in test data so I don't keep hitting gmail api
        current_emails = ['http://www.fileplanet.com/download.aspx?f=214043', 'http://netstorage.unity3d.com/unity/UnitySetup-4.3.0.exe', 'http://i.imgur.com/aw384tw.png', 'http://i.imgur.com/DCOCf91.png', 'http://i.imgur.com/g3mXqV9.png', 'http://i.imgur.com/pWj4VDX.gif', 'http://i.imgur.com/sTNT8hH.jpg,', 'http://i.imgur.com/lOOw9rq.gif', 'http://i.imgur.com/ZsvBJX2.jpg']

        #Render the mako template and pass it the current_emails list variable
        mako_template_render = mako_template.render(inbox_urls = current_emails)

        return mako_template_render

    @cherrypy.expose
    def queue(self):       
        #Create the below template using index.html (and looking up in the static folder)
        mako_template = Template(filename='static/queue.html')
        
        #[0] = Filename | [1] =Download Status | [2] = 'Queue Time'
        thequeue = [ ["Unity3D.exe", 40, "1/16/13"],
                   ["DirectX9.0.0.120.exe", 20, "1/18/13"],
                   ["Unity3D.exe", 0, "1/20/13"] ] 

        #Render the mako template and pass it the current_emails list variable
        mako_template_render = mako_template.render(queued_files = thequeue)

        return mako_template_render
        

    #index.exposed = True
    #history.exposed = True    


cherrypy.quickstart(webServer(), config=conf)