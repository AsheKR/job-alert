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
        """
        kwargs 에서는 self.result_parser 에서 필요한 추가 데이터를 받을 수 있도록 합니다.
        self.result_parser 를 사용하여 self._content 에 대입하는 코드를 작성해주세요.
        """
        raise NotImplementedError('BaseSender 는 prepare_data 를 반드시 구현해야합니다.')

    def send(self):
        """
        self._content 를 사용하여 전송해주세요.
        """
        raise NotImplementedError('BaseSender 는 send 메서드를 반드시 구현해야합니다.')
