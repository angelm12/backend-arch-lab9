from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


from app import db
from models import User
from passlib.hash import pbkdf2_sha256
from schemas import UserSchema

blp = Blueprint("users", __name__, description="User Management APIs")


@blp.route("/register")
class RegisterUser(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        hashed_password = pbkdf2_sha256.hash(user_data['password'])
        user = User(username=user_data['username'], quote=user_data['quote'], password=hashed_password)
        db.session.add(user)
        db.session.commit()

@blp.route("/login")
class LoginUser(MethodView):
    @blp.arguments(UserSchema(only=("username", "password")))
    @blp.response(200)
    def post(self, user_credentials):
        user = User.query.filter_by(username=user_credentials['username']).first()
        access_token = create_access_token(identity=user.username)
        return {"access_token": access_token}

@blp.route("/protected")
class Protected(MethodView):
    @jwt_required()
    @blp.response(200)
    def get(self):
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()
        return {"username": user.username, "quote": user.quote}