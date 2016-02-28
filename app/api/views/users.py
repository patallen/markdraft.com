from flask import request

from api import app
from api.auth import jwt
from marklib.request import MakeResponse
from models import User, schemas


documents_schema = schemas.DocumentSchema(many=True)


# REGISTRATION & LOGIN
@app.route("/auth/register", methods=['POST'])
def auth_registration():
    data = request.get_json()
    username = data.get('username')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    pass1 = data.get('password1')
    pass2 = data.get('password2')

    no_exist = User.query.filter_by(email=email).first() is None
    pass_equiv = pass1 == pass2

    xhr = MakeResponse()

    if not pass_equiv:
        xhr.set_error(422, "Paswords to not match.")
    elif not no_exist:
        xhr.set_error(409, "Email address is not available for use.")
    else:
        user = User({
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": pass1
        })
        user.save()
        xhr.set_status(200)

    return xhr.response


@app.route("/auth/login", methods=['post'])
def auth_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    xhr = MakeResponse()
    if user and user.authenticate(password):
        token = jwt.create_token_for_user(user)
        res = dict(access_token=token)
        xhr.set_body(res)
        return xhr.response

    else:
        xhr.set_error(401, {"error": "Trouble authenticating"})
        return xhr.response


# User's Document GET (ALL)
@app.route("/users/<int:user_id>/documents")
def get_user_documents(user_id):
    docs = User.query.get(user_id).documents
    docs = documents_schema.dump(docs)
    xhr = MakeResponse(body=docs.data)
    return xhr.response


# User's Tag GET (ALL)
@app.route("/users/<int:user_id>/tags")
@jwt.require_jwt
def get_user_tags(user_id):
    user = User.query.get_or_404(user_id)
    tags = user.tags
    tags = [t.to_dict() for t in tags]
    xhr = MakeResponse(body=tags)
    return xhr.response


# Get Users
@app.route("/users")
def get_users():
    users = User.query.all()
    users = [u.to_dict(include='is_admin') for u in users]
    xhr = MakeResponse(body=users)
    return xhr.response
