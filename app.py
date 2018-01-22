import cherrypy
import os
from jinja2 import Environment, FileSystemLoader
import parse

env = Environment(loader=FileSystemLoader('html'))

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        par = parse.Parse()                             #init
        equity = par.obtain()                           #fetch parsed values

        last_update = par.last_update()                 #fetch last update date

        unidict = []
        for entry in equity:
            unidict.append({key.decode('utf8'): value.decode('utf8') for key, value in entry.items()})          #decode

        tmpl = env.get_template('index.html')
        return tmpl.render(equity = unidict, last_update = last_update, heading = "Top ten entries")

    @cherrypy.expose
    def search(self, query = None):
        par = parse.Parse()                             #init
        equity = par.search(query.upper().rstrip())     #fetch parsed search file

        last_update = par.last_update()                 #fetch last update date

        print("\n\n\n")
        print (equity)
        print("\n\n\n")
        unidict = []

        if len(equity) > 0:
            unidict.append({key.decode('utf8'): value.decode('utf8') for key, value in equity.items()})         #decode

        tmpl = env.get_template('search.html')
        return tmpl.render(equity = unidict, query = query, last_update = last_update, heading = ("Results for " + query) if len(unidict) > 0 else "No matches found")

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