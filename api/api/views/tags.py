from flask import request, g, Blueprint

from api.auth import jwt
from marklib.request import MakeResponse
from data.models import Tag, schemas

from api.views.documents import documents_schema

blueprint = Blueprint('tag', __name__, url_prefix='/tags')

tag_schema = schemas.TagSchema()
tags_schema = schemas.TagSchema(many=True)


@blueprint.route("", methods=['POST'])
@jwt.require_jwt
def create_tag():
    user = g.current_user
    data = tag_schema.load(request.get_json()).data
    data["user"] = user
    tag = Tag.create(data)
    xhr = MakeResponse(201, tag.to_dict())
    return xhr.response


@blueprint.route("/<int:tag_id>")
@jwt.require_jwt
def get_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag = tag_schema.dump(tag).data
    xhr = MakeResponse(200, body=tag)
    return xhr.response


@blueprint.route("/<int:tag_id>", methods=['DELETE'])
@jwt.require_jwt
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag.delete()
    xhr = MakeResponse(200)
    return xhr.response


@blueprint.route("/<int:tag_id>/documents")
@jwt.require_jwt
def get_docs_for_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    docs = documents_schema.dump(tag.documents).data
    xhr = MakeResponse(200, body=docs)
    return xhr.response
