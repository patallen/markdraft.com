from flask import request
from api import app
from models.documents import Document
from models.users import User
from marklib.request import MakeResponse


# Document CREATE
@app.route("/documents", methods=['POST'])
def create_document():
    data = request.get_json()
    title = data.get("title")
    user_id = 3000  # get user from current_user
    doc = Document({"title": title, "user_id": user_id})
    doc.save()
    xhr = MakeResponse(201, doc.to_dict())
    return xhr.response


# Document GET, PUT, DELETE
@app.route("/documents/<int:doc_id>")
def get_document(doc_id):
    doc = Document.query.get_or_404(doc_id)
    xhr = MakeResponse(doc.to_dict(exclude="id"))
    return xhr.response


@app.route("/documents/<int:doc_id>", methods=['PUT'])
def edit_document(doc_id):
    print request
    data = request.get_json()
    doc = Document.query.get_or_404(doc_id)
    doc.title = data.get('title')
    xhr = MakeResponse(body=doc.to_dict())
    return xhr.response


# User's Document GET (ALL)
@app.route("/users/<int:user_id>/documents")
def user_documents(user_id):
    docs = User.query.get(user_id).documents
    docs = [d.to_dict()for d in docs]
    xhr = MakeResponse(body=docs)
    return xhr.response


# Document's Draft GET (ALL), CREATE
@app.route("/documents/<int:doc_id>/drafts")
def get_document_drafts(doc_id):
    drafts = Document.query.get(doc_id).drafts.all()
    drafts = [d.to_dict() for d in drafts]
    xhr = MakeResponse(body=drafts)
    return xhr.response