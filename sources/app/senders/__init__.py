from typing import List

from parsers import BaseParser


class BaseSender:
    def __init__(self, options: dict, result_parser: BaseParser):
        self.result_parser = result_parser

        self._content = None

    @property
    def content(self):
        if self._content is None:
            raise ValueError(
                'content 를 호출하기 전 반드시 prepare_data 가 호출되어야합니다.'
            )

        return self._content

    def prepare_data(self, results: List[dict], **kwargs):
        raise NotImplementedError('BaseSender 는 prepare_data 를 반드시 구현해야합니다.')

    def send(self):
        raise NotImplementedError('BaseSender 는 send 메서드를 반드시 구현해야합니다.')
