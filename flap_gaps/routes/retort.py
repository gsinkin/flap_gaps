from werkzeug.routing import Submount, Rule
from flap_gaps import app
from flap_gaps.endpoints import retort


retort_endpoints = Submount("/retort", [
        Rule("/echo", endpoint="retort.echo", methods=["POST"])])


app.url_map.add(retort_endpoints)
