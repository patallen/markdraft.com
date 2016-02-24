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


# User's Tag GET (ALL)
@app.route("/users/<int:user_id>/tags")
def get_user_tags(user_id):
    user = User.query.get_or_404(user_id)
    tags = user.tags
    tags = [t.to_dict() for t in tags]
    xhr = MakeResponse(body=tags)
    return xhr.response


# Get Users
@app.route("/users")
def get_users():
    users = User.query.all()
    users = [u.to_dict(include='is_admin') for u in users]
    xhr = MakeResponse(body=users)
    return xhr.response
