from marshmallow import Schema, fields


class JobDetailSchema(Schema):
    id = fields.Number(required=True)
    title = fields.String(required=True)

    url = fields.URL(required=True)

    meta = fields.List(fields.String())


class CompanySchema(Schema):
    id = fields.Number(required=True)
    name = fields.String(required=True)
    description = fields.String()

    meta = fields.String()

    sub_name = fields.String()
    thumb_up_count = fields.Number()

    logo = fields.URL()
    url = fields.URL(required=True)

    job_details = fields.List(fields.Nested(JobDetailSchema))
