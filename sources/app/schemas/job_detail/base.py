from marshmallow import Schema, fields


class BaseJobDetailSchema(Schema):
    """
    채용 정보를 담는 스키마
    """
    id = fields.Number(help_text='채용 ID', required=True)
    title = fields.String(help_text='채용 이름', required=True)
    url = fields.URL(help_text='채용 URL', required=True)

    meta = fields.List(fields.String(), help_text='추가 정보')
