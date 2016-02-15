from models import db
from models.mixins import AuditMixin, BaseMixin
from uuid import uuid4
from marklib.db import GUID


class Document(AuditMixin, BaseMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), default="Untitled Document")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    drafts = db.relationship('Draft', backref='documents', lazy='dynamic')

    def user_is_owner(self, user):
        return self.user == user


class Draft(AuditMixin, BaseMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'))
    version = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(120))
    body = db.Column(db.String())

    def user_is_owner(self, user):
        return self.document.user == user


class Share(BaseMixin, db.Model):
    uid = db.Column(GUID(), primary_key=True, default=uuid4)
    document_uid = db.Column(db.Integer, db.ForeignKey('document.id'))
    user_uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    read = db.Column(db.Boolean, default=False, nullable=False)
    write = db.Column(db.Boolean, default=False, nullable=False)
