from marshmallow import Schema, fields


class AuditMixin(object):
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class DraftSchema(AuditMixin, Schema):
    id = fields.Integer(dump_only=True)
    version = fields.Integer(dump_only=True)
    title = fields.String()
    body = fields.String()


class DocumentSchema(AuditMixin, Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()


class TagSchema(AuditMixin, Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()
    description = fields.String()
