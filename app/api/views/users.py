from api import app
from models.users import User
from marklib.request import MakeResponse


# User's Document GET (ALL)
@app.route("/users/<int:user_id>/documents")
def get_user_documents(user_id):
    docs = User.query.get(user_id).documents
    docs = [d.to_dict() for d in docs]
    xhr = MakeResponse(body=docs)
    return xhr.response


# Get Users
@app.route("/users")
def get_users():
    users = User.query.all()
    users = [u.to_dict(include='is_admin') for u in users]
    xhr = MakeResponse(body=users)
    return xhr.response
