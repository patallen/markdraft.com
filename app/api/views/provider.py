from api import app
from models.documents import Document
from marklib.request import MakeResponse


@app.route("/document/<int:doc_id>")
def document(doc_id):
    xhr = MakeResponse()
    doc = Document.query.get(doc_id)
    xhr.set_body(doc.to_dict(exclude="id"))
    return xhr.response()
