import os

# Flask Config
FLASK_ENV = os.environ["FLASK_ENV"]
FLASK_SECRET_KEY = os.environ["FLASK_SECRET_KEY"]

## Gunicorn Config
GUNICORN_BIND = os.environ["GUNICORN_BIND"]
GUNICORN_WORKERS = int(os.environ["GUNICORN_WORKERS"])
GUNICORN_WORKER_CLASS = os.environ["GUNICORN_WORKER_CLASS"]
GUNICORN_TIMEOUT = os.environ["GUNICORN_TIMEOUT"]
