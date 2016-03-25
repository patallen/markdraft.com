from flask import request, Blueprint

from marklib.request import MakeResponse
from data.models import Document, schemas
from api.auth import jwt
import api.helpers

blueprint = Blueprint('document', __name__, url_prefix='/documents')

document_schema = schemas.DocumentSchema()
documents_schema = schemas.DocumentSchema(many=True)


# GET documents available to user
@blueprint.route("", methods=['GET'])
@jwt.require_jwt
def get_available_docs():
    user = api.helpers.get_user()
    accessible = api.helpers.filter_by_access(
        user, Document.query.all(), 'read'
    )
    xhr = MakeResponse(200, documents_schema.dump(accessible).data)
    return xhr.response


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
    user = api.helpers.get_user()
    doc = Document.query.get_or_404((doc_id))

    xhr = MakeResponse()
    if not doc.user_has_access(user, 'read'):
        xhr.set_error(401, "Not Authorized")
        return xhr.response

    res = document_schema.dump(doc)
    xhr.set_success(data=res.data)
    return xhr.response


@blueprint.route("/<int:doc_id>", methods=['PUT'])
@jwt.require_jwt
def edit_document(doc_id):
    user = api.helpers.get_user()
    data = document_schema.load(request.get_json())
    doc = Document.query.get_or_404(doc_id)
    xhr = MakeResponse()

    if not doc.user_has_access(user, 'write'):
        xhr.set_error(401, "Not authorized to edit document.")
        return xhr.response

    for k, v in data.data.iteritems():
        setattr(doc, k, v)

    doc.save()
    xhr = MakeResponse(200, body=document_schema.dump(doc).data)
    return xhr.response


@blueprint.route("/<int:doc_id>", methods=['DELETE'])
@jwt.require_jwt
def delete_document(doc_id):
    user = api.helpers.get_user()
    doc = Document.query.get_or_404(doc_id)
    xhr = MakeResponse(200)

    if not doc.user_has_access(user, 'edit'):
        xhr.set_error(401, "Not authorized to delete document.")
        return xhr.response

    doc.delete()
    return xhr.response
