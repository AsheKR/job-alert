from marshmallow_oneofschema import OneOfSchema

from schemas import TYPE_ROCKET_PUNCH, TYPE_WANTED
from schemas.company.rocket_punch import RocketPunchCompanySchema
from schemas.company.wanted import WantedCompanySchema


class CompanyOneOfSchema(OneOfSchema):
    type_field = "object_type"
    type_schemas = {
        TYPE_ROCKET_PUNCH: RocketPunchCompanySchema,
        TYPE_WANTED: WantedCompanySchema,
    }
