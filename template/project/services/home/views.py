from flask_restx import Namespace, Resource

from project.utils.middleware import middleware

home_ns = Namespace("Home", description="Flask template home")

@home_ns.route("/")
class HomePage(Resource):

    @middleware(send_user_data=False)
    def get(self):
        return "Hello World!"
