from marshmallow import Schema, fields

from schemas.site import SiteSchema


class ResultSchema(Schema):
    keyword = fields.String(help_text='검색 키워드', required=True)
    count = fields.Number(help_text='검색 결과 개수', required=True)

    results = fields.List(fields.Nested(SiteSchema), help_text='검색 결과')
