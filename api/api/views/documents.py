from flask import request, Blueprint

from marklib.request import MakeResponse
from data.models import Document, schemas
from api.auth import jwt
import api.helpers

blueprint = Blueprint('document', __name__, url_prefix='/documents')

document_schema = schemas.DocumentSchema()
documents_schema = schemas.DocumentSchema(many=True)


# Document CREATE
@blueprint.route("", methods=['POST'])
@jwt.require_jwt
def create_document():
    user = api.helpers.get_user()
    data = document_schema.load(request.get_json()).data
    data['user'] = user
    doc = Document.create(data)
    xhr = MakeResponse(201, document_schema.dump(doc).data)
    return xhr.response


# Document GET, PUT, DELETE
@blueprint.route("/<int:doc_id>")
@jwt.require_jwt
def get_document(doc_id):
    doc = Document.query.get_or_404((doc_id))
    doc = document_schema.dump(doc)
    xhr = MakeResponse(200, body=doc.data)
    return xhr.response


@blueprint.route("/<int:doc_id>", methods=['PUT'])
@jwt.require_jwt
def edit_document(doc_id):
    data = document_schema.load(request.get_json())
    doc = Document.query.get_or_404(doc_id)
    for k, v in data.data.iteritems():
        setattr(doc, k, v)
    doc.save()
    xhr = MakeResponse(200, body=document_schema.dump(doc).data)
    return xhr.response


@blueprint.route("/<int:doc_id>", methods=['DELETE'])
@jwt.require_jwt
def delete_document(doc_id):
    doc = Document.query.get_or_404(doc_id)
    doc.delete()
    xhr = MakeResponse()
    xhr.set_status(200)
    return xhr.response
