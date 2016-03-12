from flask import Blueprint

from api.auth import jwt
from marklib.request import MakeResponse
from data.models import User, schemas

blueprint = Blueprint('user', __name__, url_prefix='/users')
documents_schema = schemas.DocumentSchema(many=True)


# User's Document GET (ALL)
@blueprint.route("/<int:user_id>/documents")
@jwt.require_jwt
def get_user_documents(user_id):
    docs = User.query.get(user_id).documents
    docs = documents_schema.dump(docs)
    xhr = MakeResponse(200, body=docs.data)
    return xhr.response


# User's Tag GET (ALL)
@blueprint.route("/<int:user_id>/tags")
@jwt.require_jwt
def get_user_tags(user_id):
    user = User.query.get_or_404(user_id)
    tags = user.tags
    tags = [t.to_dict() for t in tags]
    xhr = MakeResponse(200, body=tags)
    return xhr.response


# Get Users
@blueprint.route("")
@jwt.require_jwt
def get_users():
    users = User.query.all()
    users = [u.to_dict(include='is_admin') for u in users]
    xhr = MakeResponse(200, body=users)
    return xhr.response
