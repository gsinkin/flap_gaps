import logging
import logging.config

from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False
logging.basicConfig()

logger = logging.getLogger(__name__)
