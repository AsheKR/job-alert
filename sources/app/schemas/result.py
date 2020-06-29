from marshmallow import Schema, fields

from schemas.site import SiteSchema


class ResultSchema(Schema):
    keyword = fields.String(required=True)
    count = fields.Number(required=True)

    results = fields.List(fields.Nested(SiteSchema))
