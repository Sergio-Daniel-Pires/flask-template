from flask_restx import Namespace, Resource

from project.utils.middleware import Middleware

home_ns = Namespace("Home", description="Flask template home")

@home_ns.route("/")
class HomePage(Resource):

    @Middleware()
    def get(self):
        return "Hello World!"
