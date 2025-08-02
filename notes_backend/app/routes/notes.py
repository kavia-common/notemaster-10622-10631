from flask_smorest import Blueprint, abort
from flask.views import MethodView
from app.models import db, Note
from app.schemas import NoteSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

blp = Blueprint("Notes", "notes", url_prefix="/notes", description="Notes CRUD endpoints")

@blp.route("/")
class NoteListAPI(MethodView):
    # PUBLIC_INTERFACE
    @jwt_required()
    @blp.response(200, NoteSchema(many=True))
    def get(self):
        """List all notes for authenticated user."""
        identity = get_jwt_identity()
        notes = Note.query.filter_by(user_id=identity["user_id"]).order_by(Note.updated_at.desc()).all()
        return notes

    # PUBLIC_INTERFACE
    @jwt_required()
    @blp.arguments(NoteSchema)
    @blp.response(201, NoteSchema)
    def post(self, note_data):
        """Create a new note for authenticated user."""
        identity = get_jwt_identity()
        note = Note(title=note_data["title"], content=note_data.get("content", ""), user_id=identity["user_id"])
        db.session.add(note)
        db.session.commit()
        return note

@blp.route("/<int:note_id>")
class NoteAPI(MethodView):
    # PUBLIC_INTERFACE
    @jwt_required()
    @blp.response(200, NoteSchema)
    def get(self, note_id):
        """Get a single note by id for authenticated user."""
        identity = get_jwt_identity()
        note = Note.query.filter_by(id=note_id, user_id=identity["user_id"]).first()
        if not note:
            abort(404, message="Note not found")
        return note

    # PUBLIC_INTERFACE
    @jwt_required()
    @blp.arguments(NoteSchema)
    @blp.response(200, NoteSchema)
    def put(self, note_data, note_id):
        """Update a note if owned by the user."""
        identity = get_jwt_identity()
        note = Note.query.filter_by(id=note_id, user_id=identity["user_id"]).first()
        if not note:
            abort(404, message="Note not found")
        note.title = note_data["title"]
        note.content = note_data.get("content", "")
        db.session.commit()
        return note

    # PUBLIC_INTERFACE
    @jwt_required()
    def delete(self, note_id):
        """Delete a note if owned by the user."""
        identity = get_jwt_identity()
        note = Note.query.filter_by(id=note_id, user_id=identity["user_id"]).first()
        if not note:
            abort(404, message="Note not found")
        db.session.delete(note)
        db.session.commit()
        return {"message": "Note deleted"}
