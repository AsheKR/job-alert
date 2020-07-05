from marshmallow import Schema, fields

from schemas.company import CompanyOneOfSchema


class SiteSchema(Schema):
    type = fields.String(
        help_text='검색 사이트',
        required=True,
    )
    count = fields.Number(help_text='검색 결과 개수', required=True)

    companies = fields.List(fields.Nested(CompanyOneOfSchema), help_text='채용 회사')
