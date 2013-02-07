from werkzeug.routing import Submount, Rule
from flap_gaps import app
from flap_gaps.endpoints import static


static_endpoints = Submount("/", [
        Rule("/", defaults={'template': "index.html"},
             endpoint="static.html_endpoint")])


app.url_map.add(static_endpoints)
