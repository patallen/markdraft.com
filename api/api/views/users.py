from flask import Blueprint, request

from api import helpers
from api.auth import jwt
from marklib.request import MakeResponse
from data.models import User, schemas
from marklib.request import decorators
from marklib.db import filters


blueprint = Blueprint('user', __name__, url_prefix='/users')
documents_schema = schemas.DocumentSchema(many=True)


# User's Document GET (ALL)
@blueprint.route("/<int:user_id>/documents")
@decorators.crossdomain()
@jwt.require_jwt
def get_user_documents(user_id):
    user = helpers.get_user()
    available = helpers.filter_by_access(
        user,
        User.query.get(user_id).documents,
        permissions=('read',)
    )
    docs = documents_schema.dump(available)
    xhr = MakeResponse(200, body=docs.data)
    return xhr.response


# User's Tag GET (ALL)
@blueprint.route("/<int:user_id>/tags")
@decorators.crossdomain()
@jwt.require_jwt
def get_user_tags(user_id):
    user = helpers.get_user()
    xhr = MakeResponse()
    if user.id is not user_id:
        xhr.set_error(401)
        return xhr.response
    tags = User.query.get_or_404(user_id).tags
    tags = [t.to_dict() for t in tags]
    xhr.set_body(tags)
    return xhr.response


# Get Users
@blueprint.route("")
@decorators.crossdomain()
@jwt.require_jwt
def get_users():
    page = request.args.get('page')
    rows = request.args.get('rows')
    sort = request.args.get('sort')

    user = helpers.get_user()

    xhr = MakeResponse()
    if not user.is_admin:
        xhr.set_error(401, "You must be an admin.")
        return xhr.response

    query = User.query
    count = query.count()
    query = filters.sort_query(query, User, sort)
    query = filters.limit_and_offset(query, page=page, rows=rows)
    users = query.all()

    users = [u.to_dict(include='is_admin') for u in users]
    result = helpers.format_result(users, page, rows, count)
    xhr = MakeResponse(200, body=result)
    return xhr.response
