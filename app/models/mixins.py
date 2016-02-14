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
                primary_key = True
                break

        if primary_key:
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

    def get(self, key, default=None):
        return getattr(self, key) or default
