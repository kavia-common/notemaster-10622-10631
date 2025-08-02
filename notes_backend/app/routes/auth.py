from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask import request
from app.models import db, User
from app.schemas import UserSchema, UserRegisterSchema, UserLoginSchema
from app.auth import hash_password, authenticate_user, create_jwt_for_user
from flask_jwt_extended import jwt_required, get_jwt_identity

blp = Blueprint("Auth", "auth", url_prefix="/auth", description="User authentication endpoints")

@blp.route("/register")
class RegisterUser(MethodView):
    # PUBLIC_INTERFACE
    def post(self):
        """Register a new user."""
        schema = UserRegisterSchema()
        data = schema.load(request.json)
        if User.query.filter_by(username=data["username"]).first():
            abort(409, message="Username already exists.")
        user = User(username=data["username"], password_hash=hash_password(data["password"]))
        db.session.add(user)
        db.session.commit()
        return UserSchema().dump(user), 201

@blp.route("/login")
class LoginUser(MethodView):
    # PUBLIC_INTERFACE
    def post(self):
        """Authenticate and return JWT."""
        schema = UserLoginSchema()
        data = schema.load(request.json)
        user = authenticate_user(data["username"], data["password"])
        if not user:
            abort(401, message="Invalid username or password.")
        access_token = create_jwt_for_user(user)
        return {"access_token": access_token}

@blp.route("/profile")
class ProfileUser(MethodView):
    # PUBLIC_INTERFACE
    @jwt_required()
    def get(self):
        """Get the authenticated user's profile."""
        identity = get_jwt_identity()
        user = User.query.get(identity["user_id"])
        if not user:
            abort(404, message="User not found.")
        return UserSchema().dump(user)
