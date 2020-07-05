from marshmallow import fields

from schemas.company.base import BaseCompanySchema
from schemas.job_detail.wanted import WantedJobDetailSchema


class WantedCompanySchema(BaseCompanySchema):
    industry_name = fields.String()

    response_avg_rate = fields.Float()
    response_level = fields.String()
    response_delayed_count = fields.Number()
    response_avg_day = fields.Int()
    response_remained_count = fields.Number()
    response_type = fields.String()

    address = fields.String()

    like_count = fields.Number()

    images = fields.List(fields.URL())

    job_details = fields.List(fields.Nested(WantedJobDetailSchema))