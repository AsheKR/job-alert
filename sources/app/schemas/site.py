from marshmallow import Schema, fields, validate

from schemas.company import CompanySchema


class SiteSchema(Schema):
    TYPE_ROCKET_PUNCH = 'rocket_punch'
    TYPE_CHOICES = (
        TYPE_ROCKET_PUNCH,
    )

    type = fields.String(
        required=True,
        validate=validate.OneOf(choices=TYPE_CHOICES)
    )
    count = fields.Number(required=True)

    companies = fields.List(fields.Nested(CompanySchema))
