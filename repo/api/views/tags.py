from flask import request

from api import app
from marklib.request import MakeResponse
from models import Tag, schemas

from api.views.documents import documents_schema


tag_schema = schemas.TagSchema()
tags_schema = schemas.TagSchema(many=True)


@app.route("/tags", methods=['POST'])
def create_tag():
    data = tag_schema.load(request.get_json()).data
    user_id = 2  # get user from current_user
    tag = Tag(data)
    tag.user_id = user_id
    tag.save()
    xhr = MakeResponse(201, tag.to_dict())
    return xhr.response


@app.route("/tags/<int:tag_id>")
def get_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag = tag_schema.dump(tag).data
    xhr = MakeResponse(body=tag)
    return xhr.response


@app.route("/tags/<int:tag_id>")
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag.delete()
    xhr = MakeResponse()
    return xhr.response


@app.route("/tags/<int:tag_id>/documents")
def get_docs_for_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    docs = documents_schema.dump(tag.documents).data
    xhr = MakeResponse(body=docs)
    return xhr.response
