from flask_restx import Namespace, Resource

home_ns = Namespace("home", description="Template home endpoint")


@home_ns.route("/")
class Home(Resource):
    def get(self):
        """Small sanity check used by the frontend and by monitoring."""
        return {"result": "Hello World!", "message": "Ok"}
