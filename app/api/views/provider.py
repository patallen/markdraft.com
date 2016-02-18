from api import app
from models.documents import Document
from models.users import User
from marklib.request import MakeResponse


@app.route("/users/<int:user_id>/documents")
def user_documents(user_id):
    xhr = MakeResponse()
    docs = User.query.get(user_id).documents
    print "docs", docs
    docs = [d.to_dict()for d in docs]
    xhr.set_body(docs)
    return xhr.response


@app.route("/documents/<int:doc_id>")
def document(doc_id):
    xhr = MakeResponse()
    doc = Document.query.get(doc_id)
    xhr.set_body(doc.to_dict(exclude="id"))
    return xhr.response


@app.route("/documents/<int:doc_id>/drafts")
def document_drafts(doc_id):
    xhr = MakeResponse()
    drafts = Document.query.get(doc_id).drafts.all()
    drafts = [d.to_dict() for d in drafts]
    xhr.set_body(drafts)
    return xhr.response
