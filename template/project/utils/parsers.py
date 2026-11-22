from flask_restx import reqparse

echo_parser = reqparse.RequestParser()
echo_parser.add_argument("message", type=str, help="Message that server will echo", location="form")
echo_parser.add_argument(
    "echo_type", type=str, choices=( "None", "Reverse", "Mirror" ),
    help="Type of echo", location="form", default="None", required=True
)
