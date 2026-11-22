
from flask_restx import Namespace, Resource

from project.services.echo.methods import echo_message
from project.utils.middleware import USER_DATA, middleware
from project.utils.parsers import echo_parser

echo_ns = Namespace("Echo", description="Flask route to echo a message")

@echo_ns.route("/string")
class EchoMessage(Resource):

    @echo_ns.doc(expect=[ echo_parser ])
    @middleware()
    def post(self, user_data: USER_DATA) -> str:
        return echo_message(user_data)
