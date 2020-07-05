from typing import List

from parsers import BaseParser
from senders import BaseSender


class HTMLDebugOutputSender(BaseSender):
    def __init__(self, result_parser: BaseParser, options: dict = None, output_file_name='debug.html'):
        if options is None:
            options = {}
        super().__init__(options, result_parser)

        self.output_file_name = output_file_name
        self._title = None

    @property
    def title(self):
        if self._title is None:
            raise ValueError(
                'title 을 호출하기 전 반드시 prepare_data 가 호출되어야합니다.'
            )

        return self._title

    def prepare_data(self, results: List[dict], **kwargs):
        self._title = kwargs.get('title')
        if not self._title:
            raise ValueError(
                'HTMLDebugOutputSender 를 사용하기 위해서는 prepare_data 에 title 를 제공해야합니다.'
            )

        self._content = self.result_parser.parse(results, title=self._title, sub_title='일간 신규 채용 알리미')

    def send(self):
        with open(self.output_file_name, 'w') as f:
            f.write(self._content)
