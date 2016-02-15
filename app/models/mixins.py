from datetime import datetime
from models import db


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

    def __init__(self, data=None):
        if data is not None:
            self.update_attributes(data)

    def update_attributes(self, data):
        for k, v in data.iteritems():
            if hasattr(self, k):
                setattr(self, k, v)

    def get(self, key, default=None):
        return getattr(self, key) or default
