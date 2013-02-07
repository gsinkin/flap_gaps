import logging
from flap_gaps import app
from flap_gaps.lib.rendering import render_html_template

logger = logging.getLogger(__name__)


@app.endpoint('static.html_endpoint')
def html_endpoint(template=None):
    logger.debug("Request for static page: %s" % template)
    return render_html_template(template)
