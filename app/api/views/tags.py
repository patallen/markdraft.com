from flask import request

from api import app
from models.tags import Tag
from marklib.request import MakeResponse


@app.route("/tags", methods=['POST'])
def create_tag():
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    user_id = 3000  # get user from current_user
    tag = Tag({
        "title": title,
        "description": description,
        "user_id": user_id
    })
    tag.save()
    xhr = MakeResponse(201, tag.to_dict())
    return xhr.response


@app.route("/tags/<int:tag_id>")
def get_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    xhr = MakeResponse(body=tag.to_dict())
    return xhr.response


@app.route("/tags/<int:tag_id>/documents")
def get_docs_for_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    docs = [d.to_dict() for d in tag.documents]
    xhr = MakeResponse(body=docs)
    return xhr.response
