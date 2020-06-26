from typing import Union, List

from schemas.company import CompanySchema


class RocketPunchAdapter:
    def __init__(self, data: Union[List, dict], parser):
        self._data = data
        self._aware_data = None

        self._parser = parser

    @property
    def aware_data(self) -> Union[List, dict]:
        if not self._aware_data:
            if isinstance(self._data, List):
                schema = CompanySchema(many=True)
            else:
                schema = CompanySchema()

            self._aware_data = schema.load(self._data)

        return self._aware_data

    def to_html(self) -> str:
        parser = self._parser
        html = ''

        if isinstance(self._data, List):
            for company in self.aware_data:
                html += parser.to_html(company)
        else:
            html += parser.to_html(self._data)

        return html
