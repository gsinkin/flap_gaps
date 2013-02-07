class FlapGapsApp(object):

    def __init__(self):
        from flap_gaps import app as application
        self.application = application
        self.load_endpoints()

    def load_endpoints(self):
        from flap_gaps.routes import static
        from flap_gaps.routes import retort
