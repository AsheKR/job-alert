from marshmallow import fields

from schemas.company.base import BaseCompanySchema
from schemas.job_detail.rocket_punch import RocketPunchJobDetailSchema


class RocketPunchCompanySchema(BaseCompanySchema):
    sub_name = fields.String(help_text='회사 추가 이름')
    thumb_up_count = fields.Number(help_text='추천 개수')

    job_details = fields.List(fields.Nested(RocketPunchJobDetailSchema, help_text='채용 정보'))
