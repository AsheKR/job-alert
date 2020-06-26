class JobDetailParser:
    @staticmethod
    def to_html(data: dict):
        return f'<h3>{data.get("title")}</h3>'
