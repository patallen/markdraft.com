from sqlalchemy.orm import column_property

from data.models.mixins import AuditMixin, BaseMixin
from uuid import uuid4
from marklib.db.ext import GUID
from data import db
from werkzeug.security import (
    generate_password_hash, check_password_hash
)


class Document(AuditMixin, BaseMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), default="Untitled Document")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String())

    def user_has_access(self, user, permission='read'):
        if self.user_is_owner(user):
            return True

        share = Share.get_share(user, self)
        if share:
            return getattr(share, permission)
        return False


class Share(BaseMixin, db.Model):
    uid = db.Column(GUID(), primary_key=True, default=uuid4)
    document_id = db.Column(
        db.Integer,
        db.ForeignKey('document.id', ondelete="cascade"),
        nullable=False
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='cascade'),
        nullable=False
    )
    read = db.Column(db.Boolean, default=False, nullable=False)
    write = db.Column(db.Boolean, default=False, nullable=False)
    delete = db.Column(db.Boolean, default=False, nullable=False)
    unique = db.UniqueConstraint()

    @classmethod
    def create_or_update(
        cls,
        user,
        entity,
        read=True,
        write=False,
        commit=True,
    ):
        share = cls.get_share(user=user, entity=entity)

        if share:
            share.update_attributes({"read": read, "write": write})
        else:
            attrs = dict(
                document_id=entity.id,
                user_id=user.id,
                read=read,
                write=write,
            )
            share = Share(attrs)
        share.save(commit=commit)

        return share

    @classmethod
    def get_share(cls, user=None, entity=None):
        if not user or not entity:
            raise ValueError("User and entity required.")

        return cls.query.filter_by(user_id=user.id) \
            .filter_by(document_id=entity.id).first()

    @classmethod
    def shares_for_user_query(cls, user_id=None, user=None):
        if user is not None:
            user_id = user.id
        if user_id:
            return db.session.query(cls).filter_by(user_id=user_id)
        return None

    @classmethod
    def shares_for_user(cls, user_id=None, user=None, read=None, write=None):
        if not user_id:
            user_id = user.id
        query = cls.shares_for_user_query(user_id)

        if read is not None:
            query = query.filter_by(read=read)

        if write is not None:
            query = query.filter_by(write=write)

        if query:
            return query.all()


class User(BaseMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    username = db.Column(db.String(), unique=True)
    email = db.Column(db.String(), unique=True)
    _admin = db.Column(db.Boolean, default=False)
    _active = db.Column(db.Boolean, default=True)
    _password = db.Column(db.String(), nullable=False)

    full_name = column_property(first_name + ' ' + last_name)

    tags = db.relationship('Tag', backref='user', lazy='dynamic')

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


tags = db.Table(
    'tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('document_id', db.Integer, db.ForeignKey('document.id'))
)


class Tag(AuditMixin, BaseMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False, default="Untitled Tag")
    description = db.Column(db.String(140))
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='cascade')
    )

    documents = db.relationship(
        'Document',
        backref=db.backref('tags'),
        secondary=tags
    )
