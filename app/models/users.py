from models import db
from models.mixins import BaseMixin


class User(BaseMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    username = db.Column(db.String(), unique=True)
    email = db.Column(db.String(), unique=True)

    def owns_document(self, document):
        return document in self.documents

    documents = db.relationship('Document', backref='user', lazy='dynamic')
