from marshmallow import Schema, fields


class AuditMixin(object):
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class DraftSchema(AuditMixin, Schema):
    id = fields.Integer(dump_only=True)
    version = fields.Integer(dump_only=True)
    title = fields.String()
    body = fields.String()


class DocumentSchema(AuditMixin, Schema):
    id = fields.Integer()
    title = fields.String()
