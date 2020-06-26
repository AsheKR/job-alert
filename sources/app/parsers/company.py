class CompanyParser:
    @staticmethod
    def to_html(data: dict):
        return f'<h1>{data.get("name")}</h1>'
