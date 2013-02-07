import os
from wsgi_files import FlapGapsApp


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    FlapGapsApp().application.run(host='0.0.0.0', port=port)
