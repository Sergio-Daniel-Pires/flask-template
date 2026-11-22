import dotenv

# Load .env vars
dotenv.load_dotenv(override=False)

from flask import Flask
from flask_restx import Api

from project._version import __version__ as API_VERSION
from project.services.echo.views import echo_ns
from project.services.home.views import home_ns

# Create flask swagger API
api = Api(
    title="Flask + Swagger",
    description="A flask factories server template ready to deploy with Swagger documentation",
    version=API_VERSION,
    doc="/docs"
)

def create_app() -> Flask:
    """
    Create an app with a given name
    """

    app = Flask(__name__)

    # Add routes
    # Home routes
    api.add_namespace(home_ns, path="/home")

    # Echo routes
    api.add_namespace(echo_ns, path="/echo")

    api.init_app(app)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
