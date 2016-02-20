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

    def user_has_access(self, user, permission='read'):
        if self.user_is_owner(user):
            return True

        share = Share.get_share(user, self)
        if share:
            return getattr(share, permission)
        return False

    @property
    def latest_draft(self):
        return self.drafts.order_by(Draft.version).first()

    def get_new_draft(self):
        latest = self.latest_draft
        new_version = 1
        body = None
        if latest:
            new_version = latest.version + 1
            body = latest.body
        draft = Draft({"version": new_version, "body": body})
        self.drafts.append(draft)
        self.save()
        return draft


class Draft(AuditMixin, BaseMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(
        db.Integer,
        db.ForeignKey('document.id', ondelete="cascade")
    )
    version = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(120))
    body = db.Column(db.String())

    def user_is_owner(self, user):
        return self.document.user == user

    def user_has_access(self, user, permission='read'):
        if self.user_is_owner(user):
            return True

        share = Share.get_share(user, self.document)
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
    def shares_for_user_query(cls, user_id=None):
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

        return None
