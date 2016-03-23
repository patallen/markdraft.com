from datetime import datetime
from data import db


class AuditMixin(object):
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow(),
        onupdate=datetime.utcnow()
    )


class BaseMixin(object):
    def save(self, commit=True):
        primary_key = False
        for key in ['uid', 'id']:
            if hasattr(self, key):
                primary_key = key
                break

        if primary_key and getattr(self, primary_key):
            db.session.merge(self)
        else:
            db.session.add(self)

        if commit:
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise
        else:
            db.session.flush()

        return True

    def __init__(self, data=None, **kwargs):
        if data is None:
            data = kwargs
        if data is not None:
            self.update_attributes(data)

    def update_attributes(self, data):
        for k, v in data.iteritems():
            if hasattr(self, k):
                setattr(self, k, v)
            else:
                raise ValueError

    @classmethod
    def create(cls, data):
        obj = cls(data)
        obj.save()
        return obj

    def get(self, key, default=None):
        return getattr(self, key) or default

    def to_dict(self, exclude=None, include=None):
        include = include or []
        exclude = exclude or []
        if not isinstance(include, list):
            include = [include]
        if not isinstance(exclude, list):
            exclude = [exclude]

        cols = [k.key for k in self.__table__.columns if k.key[0] is not '_']
        attrs = [c for c in cols if c not in exclude] + include

        rv = {}
        for attr in attrs:
            if hasattr(self, attr):
                rv[attr] = unicode(getattr(self, attr))
        return rv

    def delete(self, commit=True):
        db.session.delete(self)
        if commit:
            db.session.commit()

    def user_is_owner(self, user):
        return self.user == user
