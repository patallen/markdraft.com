from flask import request, Blueprint

import api
from api.auth import jwt
from marklib.request import MakeResponse
from data.models import User

blueprint = Blueprint('auth', __name__, url_prefix='/auth')


# REGISTRATION & LOGIN
@blueprint.route("/register", methods=['POST'])
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
        xhr.set_error(422, "Paswords do not match.")
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


@blueprint.route("/login", methods=['post'])
def auth_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    xhr = MakeResponse(200)
    if user and user.authenticate(password):
        token = jwt.create_token_for_user(user)
        res = dict(access_token=token)
        xhr.set_body(res)
        return xhr.response

    else:
        xhr.set_error(401, {"error": "Trouble authenticating"})
        return xhr.response

@blueprint.route("/get_refresh_token")
def get_refresh_token():
    user = api.helpers.get_user()
    user_id = user.id
    agent = request.headers.get('User-Agent')
    token = jwt.create_refresh_token(user_id, agent)
    xhr = MakeResponse(200)
    res = dict(refresh_token=token)
    xhr.set_body(res)
    return xhr.response
