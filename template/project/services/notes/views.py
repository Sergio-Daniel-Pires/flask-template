from flask_restx import Namespace, Resource, fields
from sqlalchemy import select

from project.extensions import db
from project.services.notes.models import Note

notes_ns = Namespace("notes", description="Notes stored in SQLite")

note_input = notes_ns.model(
    "NoteInput",
    {
        "text": fields.String(
            required=True,
            max_length=500,
            description="Note content",
            example="Primeira nota",
        ),
    },
)

note_model = notes_ns.model(
    "Note",
    {
        "id": fields.Integer,
        "text": fields.String,
        "created_at": fields.String(description="ISO-8601 timestamp"),
    },
)

note_list = notes_ns.model(
    "NoteList",
    {
        "result": fields.List(fields.Nested(note_model)),
        "message": fields.String(example="Ok"),
    },
)

note_response = notes_ns.model(
    "NoteResponse",
    {
        "result": fields.Nested(note_model),
        "message": fields.String(example="Ok"),
    },
)


@notes_ns.route("/")
class NoteList(Resource):
    @notes_ns.marshal_with(note_list)
    def get(self):
        """List notes, newest first."""
        notes = db.session.scalars(select(Note).order_by(Note.id.desc())).all()
        return {
            "result": [note.to_dict() for note in notes],
            "message": "Ok",
        }

    @notes_ns.expect(note_input, validate=True)
    @notes_ns.marshal_with(note_response, code=201)
    def post(self):
        """Create a note."""
        text = (notes_ns.payload or {}).get("text", "").strip()
        if not text:
            notes_ns.abort(400, "text must not be empty")
        if len(text) > 500:
            notes_ns.abort(400, "text must be at most 500 characters")

        note = Note(text=text)
        db.session.add(note)
        db.session.commit()

        return {"result": note.to_dict(), "message": "Ok"}, 201
