from models import db
from models.mixins import AuditMixin, BaseMixin


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
