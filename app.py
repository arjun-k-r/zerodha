import cherrypy
import os
from jinja2 import Environment, FileSystemLoader
import parse

env = Environment(loader=FileSystemLoader('html'))

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return ("Zerodha: Python test task")

config = {
    'global': {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': int(os.environ.get('PORT', 5000)),
    },
    '/assets': {
        'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__)),
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'assets',
    }
}

cherrypy.quickstart(HelloWorld(), '/', config=config)