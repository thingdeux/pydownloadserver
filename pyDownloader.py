import cherrypy
import emailCrawl
from mako.template import Template

# bind to all IPv4 interfaces and set port
cherrypy.config.update({ 'server.socket_host': '0.0.0.0',
                         'server.socket_port': 12334,
                         })



class webServer(object):


    def index(self):
        mako_template = Template(filename='static/index.html')
        current_emails = emailCrawl.listAllEmails()
        mako_template_render = mako_template.render(inbox_urls = current_emails)

        return mako_template_render



    def history(self):
        return "History will go here"




    index.exposed = True
    history.exposed = True




cherrypy.quickstart(webServer())