from wsgiref.simple_server import make_server

from wunderbar.framework import WunderbarApp
from urls import routes

app = WunderbarApp(routes=routes)

with make_server('', 8080, app) as httpd:
    print(f'Starting a server on {httpd.server_name}:{httpd.server_port}')
    httpd.serve_forever()
