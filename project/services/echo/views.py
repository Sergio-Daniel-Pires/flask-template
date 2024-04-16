import json

import flask
from flask_restx import Namespace, Resource

from project.services.echo.methods import echo_message
from project.utils.middleware import Middleware
from project.utils.parsers import echo_parser

echo_ns = Namespace("Echo", description="Flask route to echo a message")

@echo_ns.route("/string")
class EchoMessage(Resource):

    @echo_ns.doc(expect=[ echo_parser ])
    @Middleware()
    def post(self):
        user_data = dict(flask.request.form)
        user_data = dict(json.loads(flask.request.data))
        user_data.update(flask.request.files)

        return echo_message(user_data)
