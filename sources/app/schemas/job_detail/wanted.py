from marshmallow import fields

from schemas.job_detail.base import BaseJobDetailSchema


class WantedJobDetailSchema(BaseJobDetailSchema):
    formatted_total = fields.String()
    formatted_recommender = fields.String()
    formatted_recommendee = fields.String()

    requirements = fields.String()
    main_tasks = fields.String()
    intro = fields.String()
    benefits = fields.String()
    preferred_points = fields.String()
