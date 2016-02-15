from models import db
from models.mixins import AuditMixin, BaseMixin


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
