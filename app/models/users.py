from werkzeug.security import (
    generate_password_hash, check_password_hash
)
from models import db
from models.mixins import BaseMixin


class User(BaseMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    username = db.Column(db.String(), unique=True)
    email = db.Column(db.String(), unique=True)
    _admin = db.Column(db.Boolean, default=False)
    _active = db.Column(db.Boolean, default=True)
    _password = db.Column(db.String(), nullable=False)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def authenticate(self, password):
        return check_password_hash(self._password, password)

    @property
    def is_admin(self):
        return self._admin

    @property
    def is_active(self):
        return self._active

    def owns_document(self, document):
        return document in self.documents

    documents = db.relationship('Document', backref='user', lazy='dynamic')
