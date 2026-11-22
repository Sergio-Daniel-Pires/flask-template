from flask_restx import Namespace, Resource, fields

from project.services.echo.methods import echo_message
from project.services.echo.models import ECHO_TYPES

echo_ns = Namespace("echo", description="Echo endpoints")

echo_input = echo_ns.model(
    "EchoInput",
    {
        "message": fields.String(
            required=True,
            max_length=10_000,
            description="Message that the server will echo",
            example="Hello world",
        ),
        "echo_type": fields.String(
            required=True,
            enum=list(ECHO_TYPES),
            default="None",
            description="How the message should be transformed",
        ),
    },
)

echo_output = echo_ns.model(
    "EchoOutput",
    {
        "result": fields.String(description="Transformed message"),
        "message": fields.String(description="Human-readable status", example="Ok"),
    },
)


@echo_ns.route("/string")
class EchoString(Resource):
    @echo_ns.expect(echo_input, validate=True)
    @echo_ns.marshal_with(echo_output)
    def post(self):
        """Echo a message, optionally reversed or mirrored."""
        payload = echo_ns.payload or {}

        try:
            result = echo_message(payload)
        except ValueError as exc:
            echo_ns.abort(400, str(exc))

        return {"result": result, "message": "Ok"}
