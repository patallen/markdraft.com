from flask import request, g

from api import app
from api.auth import jwt
from marklib.request import MakeResponse
from models import Document, schemas

drafts_schema = schemas.DraftSchema(many=True)
document_schema = schemas.DocumentSchema()
documents_schema = schemas.DocumentSchema(many=True)


# Document CREATE
@app.route("/documents", methods=['POST'])
@jwt.require_jwt
def create_document():
    user = g.current_user
    data = document_schema.load(request.get_json()).data
    doc = Document(data)
    doc.user_id = user.id
    doc.save()
    xhr = MakeResponse(201, document_schema.dump(doc).data)
    return xhr.response


# Document GET, PUT, DELETE
@app.route("/documents/<int:doc_id>")
def get_document(doc_id):
    doc = document_schema.dump(Document.query.get_or_404(doc_id))
    xhr = MakeResponse(200, body=doc.data)
    return xhr.response


@app.route("/documents/<int:doc_id>", methods=['PUT'])
def edit_document(doc_id):
    data = document_schema.load(request.get_json())
    doc = Document.query.get_or_404(doc_id)
    for k, v in data.data.iteritems():
        setattr(doc, k, v)
    doc.save()
    xhr = MakeResponse(200, body=document_schema.dump(doc).data)
    return xhr.response


@app.route("/documents/<int:doc_id>", methods=['DELETE'])
def delete_document(doc_id):
    doc = Document.query.get_or_404(doc_id)
    doc.delete()
    xhr = MakeResponse()
    xhr.set_status(200)
    return xhr.response


# Document's Draft GET (ALL), CREATE
@app.route("/documents/<int:doc_id>/drafts")
def get_document_drafts(doc_id):
    drafts = Document.query.get(doc_id).drafts.all()
    drafts = drafts_schema.dump(drafts)
    xhr = MakeResponse(body=drafts.data)
    return xhr.response
