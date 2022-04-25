from wunderbar.framework import WunderbarApp
from urls import routes

app = WunderbarApp(routes=routes)
app.run()
