from marshmallow import Schema, fields


class BaseCompanySchema(Schema):
    """
    회사 정보를 담는 스키마
    """
    id = fields.Number(help_text='회사 ID', required=True)
    name = fields.String(help_text='회사 이름', required=True)
    description = fields.String(help_text='회사 소개')

    logo_url = fields.URL(help_text='로고 이미지 URL')
    url = fields.URL(help_text='회사 소개 URL', required=True)

    meta = fields.List(fields.String(), help_text='추가 정보')
