from wsgiref.simple_server import make_server

from patterns.creational_patterns import Logger
from wunderbar.framework import WunderbarApp
from views import routes

app = WunderbarApp(routes=routes)
logger = Logger('app')

with make_server('', 8080, app) as httpd:
    logger.log(f'Starting a server on {httpd.server_name}:{httpd.server_port}')
    httpd.serve_forever()
