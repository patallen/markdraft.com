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
    user_id = user.id
    tag = Tag(data)
    tag.user_id = user_id
    tag.save()
    xhr = MakeResponse(201, tag.to_dict())
    return xhr.response


@blueprint.route("/<int:tag_id>")
def get_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag = tag_schema.dump(tag).data
    xhr = MakeResponse(200, body=tag)
    return xhr.response


@blueprint.route("/<int:tag_id>")
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag.delete()
    xhr = MakeResponse()
    return xhr.response


@blueprint.route("/<int:tag_id>/documents")
def get_docs_for_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    docs = documents_schema.dump(tag.documents).data
    xhr = MakeResponse(body=docs)
    return xhr.response
