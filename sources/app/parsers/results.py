from typing import List

from jinja2 import Environment, FileSystemLoader

from parsers import BaseParser


class HTMLResultParser(BaseParser):
    @staticmethod
    def parse(results: List[dict], **kwargs):
        title = kwargs.get('title')
        if not title:
            raise ValueError(
                'HTMLResultParser 에는 title 를 키워드 인수로 제공해야합니다.'
            )
        sub_title = kwargs.get('sub_title')

        env = Environment(
            loader=FileSystemLoader(['templates', 'static']),
        )
        template = env.get_template('index.html')

        html = template.render(
            title=title,
            sub_title=sub_title,
            results=results,
        )

        return html
